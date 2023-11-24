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
from docs_qa.prompts import generate_search_phrases_template
from docs_qa.typesense_search import typesense_retrieve_all_urls
from typing import Sequence


pp = pprint.PrettyPrinter(indent=2)

# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    search_phrase: str = Field(..., description="A relevant search phrase, in English")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    search_phrases: Sequence[RagContextRefs] = Field(..., description="List of generated search phrases.")



async def run():

    durations = {
        'query_docs': 0,
        'generate_phrases': 0,
        'store_phrases': 0,
        'total': 0
    }
    page = 1
    page_size = 3

    # Convert search phrases to vectors using all-MiniLM-L12-v2
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    total_start = start = timeit.default_timer()

    while True:
        search_response = await typesense_retrieve_all_urls(page, page_size)
        durations['query_docs'] += timeit.default_timer() - start

        print(f'typesense_retrieve_all_urls response:')
        pp.pprint(search_response)

        search_hits = [
            {
                'id': document['document']['id'],
                'url': document['document']['url_without_anchor'],
                'content_markdown': document['document']['content_markdown'],
            }
            for result in search_response['results']
            for hit in result['grouped_hits']
            for document in hit['hits']
        ]    

        print(f'Retrieved docs by url_without_anchor, page {page} (page_size={page_size})')
        pp.pprint(search_hits)

        if len(search_hits) == 0:
            break

        start = timeit.default_timer()

        doc_index = 0

        # need to preserve order in documents list
        # should only append doc if context is not too big

        while doc_index < len(search_hits):        
            search_hit = search_hits[doc_index]
            doc_index += 1

            print(f'Starting generate search phrases chain, llm: {cfg.MODEL_TYPE}')
            
            start = timeit.default_timer()
            llm = build_llm()
            prompt = ChatPromptTemplate.from_messages(
                    [('system', 'You are a helpful assistant.'),
                    ('human',  generate_search_phrases_template)]
                )

            runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
            result = runnable.invoke({
                "document": yaml.dump(search_hit.get('content_markdown',''))
            })
            durations['generate_phrases'] += timeit.default_timer() - start
            durations['total'] += timeit.default_timer() - total_start

            print(f'runnable result:')
            pp.pprint(result)

            if result['function'] is not None:
                search_phrases = [{
                    'search_phrase': context.search_phrase,
                }
                for context in result['function'].search_phrases]
            else:
                search_phrases = []

            print(f'Generated search phrases for: {search_hit["url"]}\n')
            for phrase in search_phrases:
                print(phrase)
            
        page += 1

    return None
