import box
import timeit
import yaml
import pprint
import requests
import json

from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from docs_qa.llm import build_llm
from docs_qa.prompts import qa_template
from docs_qa.extract_search_terms import run_query_async
from docs_qa.translate_answer import translate_to_language
import docs_qa.typesense_search as search
from typing import Sequence
from utils.general import scoped_env_var, env_full_name
from .config import config, azure_client, openai_client
from utils.general import is_valid_url

pp = pprint.PrettyPrinter(indent=2)

stage_name = 'DOCS_QA_RAG'
env_var = scoped_env_var(stage_name)
cfg = config()
azureClient = azure_client()
openaiClient = openai_client()


class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    source: str = Field(..., description="The metadata.source property")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    helpful_answer: str = Field(..., description="The helpful answer")
    i_dont_know: bool = Field(..., description="True when unable to answer based on the given context.")
    relevant_contexts: Sequence[RagContextRefs] = Field(..., description="List of context documents that were relevant when answering the question.")
    


async def rag_with_typesense(user_input, user_query_language_name, extract_sources=True, stream_callback=None):

    durations = {
        'total': 0,
        'analyze': 0,
        'generate_searches': 0,
        'execute_searches': 0,
        'phrase_similarity_search': 0,
        'colbert_rerank': 0,
        'rag_query': 0,
        'translation': 0,
    }
    total_start = start = timeit.default_timer()
    extract_search_queries = await run_query_async(user_input)
    durations['generate_searches'] = round(timeit.default_timer() - start, 1)


    start = timeit.default_timer()
    search_phrase_hits = await search.lookup_search_phrases_similar(extract_search_queries)
    durations['phrase_similarity_search'] = round(timeit.default_timer() - start, 1)

    print(f'Search phrase hits found: {len(search_phrase_hits)}')
    # pp.pprint(search_phrase_hits)

    start = timeit.default_timer()
    search_response = await search.typesense_retrieve_all_by_url(search_phrase_hits)
    durations['execute_searches'] = round(timeit.default_timer() - start, 1)

    search_hits = [
        {
            'id': document['document']['id'],
            'url': document['document']['url_without_anchor'],
            'lvl0': document['document']['hierarchy.lvl0'],
            'content_markdown': document['document'].get('content_markdown', ''),
        }
        for result in search_response['results']
        for hit in result['grouped_hits']
        for document in hit['hits']
    ]    

    # print(f'All source document urls:')
    # pp.pprint(search_hits)

    start = timeit.default_timer()

    all_urls = []
    all_docs = []
    loaded_docs = []
    loaded_urls = []
    loaded_search_hits = []
    doc_index = 0
    docs_length = 0

    # make list of all markdown content
    while doc_index < len(search_hits):        
        search_hit = search_hits[doc_index]
        doc_index += 1
        unique_url = search_hit['url']

        if unique_url in all_urls:
            continue

        doc_md = search_hit['content_markdown']
        if len(doc_md) == 0:
            continue

        loaded_doc = {
            'page_content': doc_md,
            'metadata': {            
                'source': unique_url,                                
            }
        }    
        all_docs.append(loaded_doc)
        all_urls.append(unique_url)


    # rerank results using ColBERT

    if env_var('COLBERT_RERANK_IN_PROCESS') == True:
        start = timeit.default_timer()
        content_original_rank = [
            document['content_markdown'][:int(cfg.MAX_SOURCE_LENGTH / 3)]
            for document in search_hits
        ]
        reranked = RAG.rerank(query=user_input, documents=content_original_rank, k=10)
    else:        
        start = timeit.default_timer()
        content_original_rank = [
            document['content_markdown'][:int(cfg.MAX_SOURCE_LENGTH / 3)]
            for document in search_hits
        ]

        rerank_url = env_var('COLBERT_API_URL')
        if not is_valid_url(rerank_url):
            raise ValueError(f"Environment variable '{env_full_name('COLBERT_API_URL')}' is invalid: '{rerank_url}'")

        rerank_data = {
            'user_input': user_input,
            'documents': content_original_rank
        }
        rerank_response = requests.post(rerank_url, data=json.dumps(rerank_data))

        # check response 200 OK
        if rerank_response.status_code != 200:
            raise Exception(f"ColBERT Rerank API request failed with status code: {rerank_response.status_code}")

        reranked = rerank_response.json()


    durations['colbert_rerank'] = round(timeit.default_timer() - start, 1)

    if env_var('LOG_LEVEL') == 'debug':
        print(f'ColBERT re-ranking results:')
        pp.pprint(reranked)

    # re-order search-hits based on new ranking
    search_hits_reranked = []
    for r in reranked:
        h = search_hits[r['result_index']]
        search_hits_reranked.append(h)


    # need to preserve order in documents list
    # should only append doc if context is not too big
    doc_index = 0

    while doc_index < len(search_hits_reranked):        
        search_hit = search_hits_reranked[doc_index]
        doc_index += 1
        unique_url = search_hit['url']

        if unique_url in loaded_urls:
            continue

        doc_md = search_hit['content_markdown']
        doc_trimmed = doc_md[:cfg.MAX_SOURCE_LENGTH]
        if (docs_length + len(doc_trimmed)) > cfg.MAX_CONTEXT_LENGTH:
            doc_trimmed = doc_trimmed[:cfg.MAX_CONTEXT_LENGTH - docs_length - 20]

        if len(doc_trimmed) == 0:
            break

        loaded_doc = {
            'page_content': doc_trimmed,
            'metadata': {            
                'source': unique_url,                                
            }
        }    
        print(f'loaded markdown doc, length= {len(doc_trimmed)}, url= {unique_url}')
        # pp.pprint(loaded_doc)

        docs_length += len(doc_trimmed)
        loaded_docs.append(loaded_doc)
        loaded_urls.append(unique_url)
        loaded_search_hits.append(search_hit)        

        if docs_length >= cfg.MAX_CONTEXT_LENGTH:
            print(f'MAX_CONTEXT_LENGTH: {cfg.MAX_CONTEXT_LENGTH} exceeded, loaded {len(loaded_docs)} docs.')
            break

        if len(loaded_docs) >= cfg.MAX_CONTEXT_DOC_COUNT:
            break

    not_loaded_urls = []
    for hit in search_hits:
        url = hit['url']
        if url not in loaded_urls and url not in not_loaded_urls:
            not_loaded_urls.append(url)


    # print(f'stuffed source document urls:')
    # pp.pprint(loaded_urls)

    print(f'Starting RAG structured output chain, llm: {cfg.MODEL_TYPE}')
    
    start = timeit.default_timer()
    llm = build_llm(streaming=False)
    prompt = ChatPromptTemplate.from_messages(
            [('system', 'You are a helpful assistant.'),
             ('human',  qa_template(user_query_language_name))]
        )

    if extract_sources:
        runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
        runnable_response = runnable.invoke({
            "context": yaml.dump(loaded_docs),
            "question": user_input
        })

        # print(f"Time to run RAG structured output chain: {chain_end - chain_start} seconds")

        # print(f'runnable result:')
        # pp.pprint(result)

        if runnable_response['function'] is not None:
            relevant_sources = [{
                'url': context.source,
                'title': next((hit['lvl0'] for hit in search_hits if hit['url'] == context.source), None),
            }
            for context in runnable_response['function'].relevant_contexts]
            rag_success = runnable_response['function'].i_dont_know != True
        else:
            relevant_sources = []
            # rag_success = None
        english_answer = runnable_response['function'].helpful_answer
        translated_answer = runnable_response['function'].helpful_answer

    else:
        full_prompt = qa_template(user_query_language_name).format(context=yaml.dump(loaded_docs), question=user_input)
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {"role": "user", "content": full_prompt },
        ]
        streaming_enabled = callable(stream_callback)

        if not streaming_enabled:
            if env_var('USE_AZURE_OPENAI_API') == True:
                chat_response = azureClient.chat.completions.create(
                    model=env_var('AZURE_OPENAI_DEPLOYMENT'),
                    temperature=0.1,
                    max_retries=0,  
                    messages=messages              
                )
            else:
                print(f"{stage_name} model name: {env_var('OPENAI_API_MODEL_NAME')}")
                chat_response = openaiClient.chat.completions.create(
                    model=env_var('OPENAI_API_MODEL_NAME'),
                    temperature=0.1,
                    max_retries=0,
                    messages=messages
                )
            english_answer = chat_response.choices[0].message.content
            translated_answer = english_answer
            rag_success = True
            relevant_sources = []
        else:
            content_so_far = ''
            chunk_count = 0
            last_callback = timeit.default_timer()

            if env_var('USE_AZURE_OPENAI_API') == True:
                for chunk in azureClient.chat.completions.create(
                                model=env_var('AZURE_OPENAI_DEPLOYMENT'),
                                temperature=0.1,
                                max_retries=0,
                                messages=messages,
                                stream=True):
                    
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        content_so_far += content
                        chunk_count += 1

                    if timeit.default_timer() - last_callback > 5:
                        last_callback = timeit.default_timer()
                        stream_callback(content_so_far)
                        
            else:
                print(f"{stage_name} model name: {env_var('OPENAI_API_MODEL_NAME')}")
                for chunk in openaiClient.chat.completions.create(
                                model=env_var('OPENAI_API_MODEL_NAME'),
                                temperature=0.1,
                                max_retries=0,
                                messages=messages,
                                stream=True):
                    
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        content_so_far += content
                        chunk_count += 1

                    if timeit.default_timer() - last_callback > 5:
                        last_callback = timeit.default_timer()
                        stream_callback(content_so_far)

            english_answer = content_so_far
            translated_answer = english_answer
            rag_success = True
            relevant_sources = []


    durations['rag_query'] = round(timeit.default_timer() - start, 1)



    start = timeit.default_timer()    
    # perhaps move this to a config flag

    translation_enabled = True

    # translate if necessary
    if translation_enabled and rag_success and  user_query_language_name != 'English':
        translated_answer = await translate_to_language(
            english_answer, user_query_language_name)
    
    durations['translation'] = round(timeit.default_timer() - start, 1)
    durations['total'] = round(timeit.default_timer() - total_start, 1)


    response = {
        'english_user_query': user_input,
        'user_query_language_name': user_query_language_name,
        'english_answer': english_answer,
        'translated_answer': translated_answer,
        'rag_success': rag_success,
        'search_queries': extract_search_queries.searchQueries,
        'source_urls': loaded_urls,
        'source_documents': loaded_docs,
        'relevant_urls': relevant_sources,
        'not_loaded_urls': not_loaded_urls,
        'durations': durations,
    }

    # pp.pprint(response)

    return response