import box
import timeit
import yaml
import asyncio
import argparse
import typesense
import pprint
import tempfile
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredMarkdownLoader
from dotenv import find_dotenv, load_dotenv
from docs_qa.chain import setup_dbqa, build_llm
from docs_qa.prompts import qa_template
from docs_qa.extract_search_terms import run_query_async
from .html_to_markdown import html_to_markdown

# Load environment variables from .env file
load_dotenv(find_dotenv())

pp = pprint.PrettyPrinter(indent=2)


# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

async def docs_query(user_input):
        # Setup DBQA
    dbqa = setup_dbqa()
    print(f'user_input:', user_input)
    response = dbqa({'query': user_input})
    return response

async def typesense_search_by_terms(search_terms):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    multi_search_args = {
        "searches":[
            {
                "collection":"altinn-studio-docs",                
                "q": (" ".join(search_terms)),
                "query_by":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,hierarchy.lvl5,hierarchy.lvl6,content",
                "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,hierarchy.lvl5,hierarchy.lvl6,content,anchor,url_without_anchor,type,id",
                "group_by":"url_without_anchor",
                "group_limit":5,
                "limit": 4,
                "sort_by":"item_priority:desc",
                # "snippet_threshold":8,
                "highlight_affix_num_tokens":4
            }   ]   
        }

    response = client.multi_search.perform(multi_search_args, {})
    return response

async def typesense_retrieve_all_by_url(url_list):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    url_searchs = [
        {
            "collection":"altinn-studio-docs",                
            "q": url,
            "query_by":"url_without_anchor",
            "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,hierarchy.lvl5,hierarchy.lvl6,content,anchor,url,url_without_anchor,type,id",
            "group_by":"url_without_anchor",
            "filter_by": "type:=content",
            # "sort_by":"item_priority:desc",
            # "snippet_threshold":8,
            "per_page": 30
        } 
        for url in url_list
    ]

    pp.pprint(url_searchs)

    # multi_search_args = { "searches": url_searchs }

    if len(url_searchs) > 1:
        url_searchs = url_searchs[:1]
    multi_search_args = { "searches": url_searchs }

    response = client.multi_search.perform(multi_search_args, {})
    return response


async def rag_with_typesense(user_input):
    extract_search_terms = await run_query_async(user_input)
    # pp.pprint(extract_search_terms)
    search_response = await typesense_search_by_terms(extract_search_terms.searchTerms)
    # pp.pprint(search_response)

    documents = [
        {
            'id': document['document']['id'],
            'url': document['document']['url_without_anchor']
        }
        for result in search_response['results']
        for hit in result['grouped_hits']
        for document in hit['hits']
    ]    

    # print(f'Document IDs')
    # pp.pprint(documents)

    unique_urls = list(set([document['url'] for document in documents]))
    print(f'Unique URLs')
    pp.pprint(unique_urls)

    # download source HTML and convert to markdown - should be done by scraper    
    with tempfile.TemporaryDirectory() as temp_dir:
        md_docs = [
            {
                'markdown': await html_to_markdown(unique_url, "#body-inner"),
                'url': unique_url,
                'file_path': os.path.join(temp_dir, unique_url.replace('/', '_').replace('https:', '') + '.md')
            }
            for unique_url in unique_urls
        ]
        # print(f'html_to_md docs:')
        # pp.pprint(md_docs)
        
        loaded_docs = []

        for doc in md_docs:
            with open(doc['file_path'], 'w') as f:
                f.write(doc['markdown'])
                f.flush()
                loaded_doc = UnstructuredMarkdownLoader(doc['file_path']).load()[0]
                loaded_docs.append(loaded_doc)
               

        # print(f'loaded markdown docs')
        # pp.pprint(loaded_docs)

    llm = build_llm()
    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
    response = chain.run(input_documents=loaded_docs, question=user_input)

    return response

def main(user_input):

    start = timeit.default_timer()
    # response = asyncio.run(docs_query(user_input))
    # print(f'docs_query response:')
    # pp.pprint(response)

    response = asyncio.run(rag_with_typesense(user_input))

    print('stuff chain response:')
    pp.pprint(response)

    end = timeit.default_timer()

    # print(f'\nAnswer: {response["result"]}')
    # print('='*50)

    # # Process source documents
    # source_docs = response['source_documents']
    # for i, doc in enumerate(source_docs):
    #     print(f'\nSource Document {i+1}\n')
    #     print(f'Source Text: {doc.page_content}')
    #     print(f'Document Name: {doc.metadata["source"]}')
    #     print(f'Metadata: {doc.metadata}')
    #     print('='* 60)

    print(f"Time to retrieve response: {end - start} seconds")
