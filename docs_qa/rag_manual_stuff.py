import box
import timeit
import yaml
import pprint

from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from docs_qa.chains import build_llm
from docs_qa.prompts import qa_template
from docs_qa.extract_search_terms import run_query_async
from .html_to_markdown import html_to_markdown
from docs_qa.typesense import typesense_search_multiple
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

    durations = {
        'generate_searches': 0,
        'execute_searches': 0,
        'download_docs': 0,
        'rag_query': 0,
        'total': 0
    }
    total_start = start = timeit.default_timer()
    extract_search_queries = await run_query_async(user_input)
    durations['generate_searches'] = timeit.default_timer() - start

    # print(f'generated queries:')
    # pp.pprint(extract_search_queries)

    start = timeit.default_timer()
    search_response = await typesense_search_multiple(extract_search_queries)
    durations['execute_searches'] = timeit.default_timer() - start

    # print(f'search response:')
    # pp.pprint(search_response)

    search_hits = [
        {
            'id': document['document']['id'],
            'url': document['document']['url_without_anchor']
        }
        for result in search_response['results']
        for hit in result['grouped_hits']
        for document in hit['hits']
    ]    

    # print(f'Document IDs')
    # pp.pprint(search_hits)

    start = timeit.default_timer()
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

        if docs_length + len(loaded_doc['page_content']) > cfg.MAX_CONTEXT_LENGTH:
            break

        docs_length += len(loaded_doc['page_content'])
        loaded_docs.append(loaded_doc)
        loaded_urls.append(unique_url)
        loaded_search_hits.append(search_hit)                


        
    durations['download_docs'] = timeit.default_timer() - start

    print(f'Starting RAG structured output chain, llm: {cfg.MODEL_TYPE}')
    
    start = timeit.default_timer()
    llm = build_llm()
    prompt = ChatPromptTemplate.from_messages(
            [('system', 'You are a helpful assistant.'),
             ('human',  qa_template)]
        )

    runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
    result = runnable.invoke({
        "context": yaml.dump(loaded_docs),
        "question": user_input
    })
    durations['rag_query'] = timeit.default_timer() - start
    durations['total'] = timeit.default_timer() - total_start

    # print(f"Time to run RAG structured output chain: {chain_end - chain_start} seconds")

    # print(f'runnable result:')
    # pp.pprint(result)

    relevant_sources = [context.source for context in result['function'].relevant_contexts]

    response = {
        'result': result['function'].helpful_answer,        
        'llm_rag_feedback': relevant_sources,
        'source_documents': loaded_docs,
        'source_urls': loaded_urls,
        'search_queries': extract_search_queries.searchQueries,
        'durations': durations
    }

    # pp.pprint(response)

    return response