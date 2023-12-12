import os
import box
import timeit
import yaml
import pprint
import typesense
import datetime

from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from docs_qa.chains import build_llm
from docs_qa.prompts import generate_search_phrases_template
import docs_qa.typesense_search as search
from typing import Sequence
from .config import config

pp = pprint.PrettyPrinter(indent=2)
cfg = config()


class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    search_phrase: str = Field(..., description="A relevant search phrase, in English")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    search_phrases: Sequence[RagContextRefs] = Field(..., description="List of generated search phrases.")


async def run(collection_name_tmp):

    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    if collection_name_tmp == None or len(collection_name_tmp) == 0:
        collection_name_tmp = f'{cfg.DOCS_SEARCH_PHRASE_COLLECTION}_{int(datetime.datetime.now().timestamp())}'

    search.setup_search_phrase_schema(collection_name_tmp)

    durations = {
        'query_docs': 0,
        'generate_phrases': 0,
        'store_phrases': 0,
        'total': 0
    }
    page = 1
    page_size = 10

    # Convert search phrases to vectors using all-MiniLM-L12-v2
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    total_start = start = timeit.default_timer()

    while True:

        print(f'Retrieving content_markdown for all urls, page {page} (page_size={page_size})')

        search_response = await search.typesense_retrieve_all_urls(page, page_size)
        durations['query_docs'] += timeit.default_timer() - start

        # print(f'typesense_retrieve_all_urls response:')
        # pp.pprint(search_response)

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

        print(f'Retrieved {len(search_hits)} urls.')
        # print(f'Retrieved docs by url_without_anchor, page {page} (page_size={page_size})')
        # pp.pprint(search_hits)

        if len(search_hits) == 0:
            print(f'Last page with results was page {page - 1}')
            break

        start = timeit.default_timer()

        doc_index = 0

        # need to preserve order in documents list
        # should only append doc if context is not too big

        while doc_index < len(search_hits):        
            search_hit = search_hits[doc_index]
            url = search_hit.get("url", "")
            doc_index += 1
            lookup_results = await search.lookup_search_phrases(url, collection_name_tmp)
            existing_phrases = lookup_results["results"][0]

            # pp.pprint(existing_phrases)

            if existing_phrases.get('found', 0) > 0:
                print(f'Found existing phrases, skipping for url: {url}')                
                continue

            print(f'Generating search phrases for url: {url}')
            
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

            # print(f'runnable result:')
            # pp.pprint(result)

            if result['function'] is not None:
                search_phrases = [{
                    'search_phrase': context.search_phrase,
                }
                for context in result['function'].search_phrases]
            else:
                search_phrases = []

            print(f'Generated search phrases for: {url}\n')

            upload_batch = []
            
            
            for index, phrase in enumerate(search_phrases):
                print(phrase)
                batch = {
                    'doc_id': search_hit.get('id',''),
                    'url': url,
                    'search_phrase': phrase.get('search_phrase', ''),
                    'sort_order': index,
                    'item_priority': 1,
                }
                upload_batch.append(batch)

            results = client.collections[collection_name_tmp].documents.import_(upload_batch, {'action': 'upsert', 'return_id': True})
            failed_results = [result for result in results if not result['success']]
            if len(failed_results) > 0:
                print(f'The following search_phrases were not successfully upserted to typesense:\n{failed_results}')
            
        page += 1

    

    return None


def commit_tmp_collection(client: typesense.Client, collection_name_tmp: str):
        """Update alias to point to new collection"""
        old_collection_name = None
        alias_name = cfg.DOCS_SEARCH_PHRASE_COLLECTION

        try:
            old_collection_name = client.aliases[alias_name].retrieve()['collection_name']
        except typesense.exceptions.ObjectNotFound:
            pass

        client.aliases.upsert(alias_name, {'collection_name': collection_name_tmp})

        # if old_collection_name:
        #     client.collections[old_collection_name].delete()