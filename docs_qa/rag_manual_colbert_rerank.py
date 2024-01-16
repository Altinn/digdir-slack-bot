import box
import timeit
import yaml
import pprint

from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from ragatouille import RAGPretrainedModel
from docs_qa.llm import build_llm
from docs_qa.prompts import qa_template
from docs_qa.extract_search_terms import run_query_async
from docs_qa.translate_answer import translate_to_language
import docs_qa.typesense_search as search
from typing import Sequence
from .config import config

pp = pprint.PrettyPrinter(indent=2)

cfg = config()


# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

RAG = RAGPretrainedModel.from_index(".ragatouille/colbert/indexes/docs-altinn-studio-colbert")



class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    source: str = Field(..., description="The metadata.source property")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    helpful_answer: str = Field(..., description="The helpful answer")
    i_dont_know: bool = Field(..., description="True when unable to answer based on the given context.")
    relevant_contexts: Sequence[RagContextRefs] = Field(..., description="List of context documents that were relevant when answering the question.")
    


async def rag_with_typesense(user_input):

    durations = {
        'total': 0,
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

    # print(f'Query language code: \'{extract_search_queries.userInputLanguageCode}\', name: \'{extract_search_queries.userInputLanguageName}\'')
    # print(f'User query, translated to English: {extract_search_queries.questionTranslatedToEnglish}')
    
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
    start = timeit.default_timer()
    content_original_rank = [
        document['content_markdown']        
        for document in search_hits
    ]
    reranked = RAG.rerank(query=user_input, documents=content_original_rank, k=10)
    durations['colbert_rerank'] = round(timeit.default_timer() - start, 1)

    # print(f'ColBERT re-ranking results:')
    # pp.pprint(reranked)

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
             ('human',  qa_template(extract_search_queries.userInputLanguageName))]
        )


    runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
    result = runnable.invoke({
        "context": yaml.dump(loaded_docs),
        "question": extract_search_queries.questionTranslatedToEnglish
    })


    durations['rag_query'] = round(timeit.default_timer() - start, 1)

    # print(f"Time to run RAG structured output chain: {chain_end - chain_start} seconds")

    # print(f'runnable result:')
    # pp.pprint(result)

    if result['function'] is not None:
        relevant_sources = [{
            'url': context.source,
            'title': next((hit['lvl0'] for hit in search_hits if hit['url'] == context.source), None),
        }
        for context in result['function'].relevant_contexts]
        rag_success = result['function'].i_dont_know != True
    else:
        relevant_sources = []
        # rag_success = None

    start = timeit.default_timer()
    
    # perhaps move this to a config flag
    translated_answer = result['function'].helpful_answer

    translation_enabled = True

    # translate if necessary
    if translation_enabled and rag_success and  extract_search_queries.userInputLanguageCode != 'en':
        translated_answer = await translate_to_language(
            result['function'].helpful_answer, extract_search_queries.userInputLanguageName)
    
    durations['translation'] = round(timeit.default_timer() - start, 1)
    durations['total'] = timeit.default_timer() - total_start


    response = {
        'original_user_query': user_input,
        'english_user_query': extract_search_queries.questionTranslatedToEnglish,
        'user_query_language_code': extract_search_queries.userInputLanguageCode,
        'user_query_language_name': extract_search_queries.userInputLanguageName,
        'english_answer': result['function'].helpful_answer,
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