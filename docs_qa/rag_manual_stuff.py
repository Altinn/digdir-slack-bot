import box
import timeit
import yaml
import pprint
import tempfile
import os

from langchain.pydantic_v1 import BaseModel, Field
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from langchain.document_loaders import UnstructuredMarkdownLoader
from docs_qa.chain import build_llm
from docs_qa.prompts import qa_template
from docs_qa.extract_search_terms import run_query_async
from .html_to_markdown import html_to_markdown
from docs_qa.typesense import typesense_search_by_terms
from typing import Sequence



pp = pprint.PrettyPrinter(indent=2)

# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    source: str = Field(..., description="The metadata.source property")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    helpful_answer: str = Field(..., description="The helpful answer")
    relevant_contexts: Sequence[RagContextRefs] = Field(..., description="List of context documents that were relevant when answering the question.")



async def rag_with_typesense(user_input):
    extract_search_terms = await run_query_async(user_input)
    pp.pprint(extract_search_terms)
    search_response = await typesense_search_by_terms(extract_search_terms.searchTerms)
    pp.pprint(search_response)

    search_hits = [
        {
            'id': document['document']['id'],
            'url': document['document']['url_without_anchor']
        }
        for result in search_response['results']
        for hit in result['grouped_hits']
        for document in hit['hits']
    ]    

    print(f'Document IDs')
    pp.pprint(search_hits)

    # unique_urls = list(set([document['url'] for document in documents]))
    # print(f'Unique URLs')
    # pp.pprint(unique_urls)

    download_start = timeit.default_timer()
    # download source HTML and convert to markdown - should be done by scraper    

    loaded_docs = []
    loaded_urls = []
    loaded_search_hits = []
    doc_index = 0
    docs_length = 0

    # need to preserve order in documents list
    # should only download doc if context is not too big

    while doc_index < len(search_hits):        
        search_hit = search_hits[doc_index]
        doc_index += 1
        unique_url = search_hit['url']

        if unique_url in loaded_urls:
            continue

        loaded_doc = {
            'page_content': await html_to_markdown(unique_url, "#body-inner"),    
            'metadata': {            
                'source': unique_url,                                
            }
        }    

        if docs_length + len(loaded_doc['page_content']) > 15000:
            break

        docs_length += len(loaded_doc['page_content'])
        loaded_docs.append(loaded_doc)
        loaded_urls.append(unique_url)
        loaded_search_hits.append(search_hit)                


        
    download_end = timeit.default_timer()    
    print(f"Time to download and convert source URLs: {download_end - download_start} seconds")

    print(f'Starting load_qa_chain...')
    chain_start = timeit.default_timer()

    llm = build_llm()

    # prompt = RagPrompt()    
    # prompt.system_prompt = 'You are a helpful assistant.'
    # prompt.bot_prompt = qa_template
    # prompt.context = yaml.dump(loaded_docs)
    # prompt.user_input = user_input

    prompt = ChatPromptTemplate.from_messages(
            [('system', 'You are a helpful assistant.'),
             ('human',  qa_template)]
        )

    runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
    result = runnable.invoke({
        "context": yaml.dump(loaded_docs),
        "question": user_input
    })

    print(f'runnable result:')
    pp.pprint(result)

    # chain = load_qa_chain(llm, chain_type="stuff", verbose=False)
    # result = chain.run(input_documents=loaded_docs, question=user_input)

    chain_end = timeit.default_timer()

    response = {
        'result': result['function'].helpful_answer,
        'llm_rag_feedback': result['function'].relevant_contexts,
        'source_documents': loaded_docs,
        'source_urls': loaded_urls,
        'search_terms': extract_search_terms.searchTerms,
    }
    print(f"Time to run load_qa_chain: {chain_end - chain_start} seconds")

    pp.pprint(response)

    return response