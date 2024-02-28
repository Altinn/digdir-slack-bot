import os
import time
import timeit
import yaml
import pprint
import typesense
import datetime
import hashlib

from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_structured_output_chain
)
from docs_qa.llm import build_llm
from docs_qa.prompts import generate_search_phrases_template
import docs_qa.typesense_search as search
from typing import Sequence
from .config import config
from utils.general import env_var

pp = pprint.PrettyPrinter(indent=2)
cfg = config()


class RagContextRefs(BaseModel):
    # relevant_content: str = Field(..., description="Three or four sentences from the most relevant parts of the context document")
    search_phrase: str = Field(..., description="A relevant search phrase, in English")

class RagPromptReply(BaseModel):
    """Relevant context data"""
    search_phrases: Sequence[RagContextRefs] = Field(..., description="List of generated search phrases.")

async def lookup_search_phrases(url, collection_name_tmp):
    retry_count = 0

    while True:
        try:
            lookup_results = await search.lookup_search_phrases(url, collection_name_tmp)
            existing_phrases = lookup_results["results"][0]
            return existing_phrases
        except Exception as e:
            print(f'Exception occured while lookup up search phrases for url: {url}\n Error: {e}')            
            if retry_count < 10:
                pass
                retry_count += 1
                time.sleep(5)
                continue
            else: 
                raise
    
async def generate_search_phrases(search_hit):
    retry_count = 0

    while True:
        try:
            llm = build_llm()
            prompt = ChatPromptTemplate.from_messages(
                    [('system', 'You are a helpful assistant.'),
                    ('human',  generate_search_phrases_template)]
                )

            runnable = create_structured_output_chain(RagPromptReply, llm, prompt)
            result = runnable.invoke({
                "document": yaml.dump(search_hit.get('content_markdown',''))
            })
            return result
        except Exception as e:
            print(f'Exception occured while generating search phrases for url: {search_hit.get("url", "")}\n Error: {e}')            
            if retry_count < 10:
                pass
                retry_count += 1
                time.sleep(5)
                continue
            else:
                raise


async def run(collection_name_tmp):

    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    if collection_name_tmp == None or len(collection_name_tmp) == 0:
        collection_name_tmp = f'{env_var("TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION")}_{int(datetime.datetime.now().timestamp())}'

    search.setup_search_phrase_schema(collection_name_tmp)

    durations = {
        'total': 0,
        'query_docs': 0,
        'generate_phrases': 0,
        'store_phrases': 0,
    }
    page = 1
    page_size = 10

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
                'content_markdown': document['document'].get('content_markdown', ''),
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

            existing_phrases = await lookup_search_phrases(url, collection_name_tmp)
            # pp.pprint(existing_phrases)

            content_md = search_hit.get('content_markdown','')
            checksum_md = hashlib.sha1(content_md.encode()).hexdigest() if content_md else None

            existing_phrase_count = existing_phrases.get('found', 0)

            if existing_phrase_count > 0:
                stored_checksum = existing_phrases.get('hits', [])[0].get('document', {}).get('checksum', '')
                checksum_matches = stored_checksum == checksum_md

                if checksum_matches:
                    print(f'Found existing phrases and checksum matches, skipping for url: {url}')            
                    doc_index += 1      
                    continue

            if existing_phrases.get('checksum', '') == checksum_md:
                print(f'Found existing phrases and checksum matches, skipping for url: {url}')            
                doc_index += 1    
                continue

            print(f'Generating search phrases for url: {url}')
            
            start = timeit.default_timer()

            result = await generate_search_phrases(search_hit)

            durations['generate_phrases'] += timeit.default_timer() - start
            durations['total'] += round(timeit.default_timer() - total_start, 1)

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

            # delete existing search phrases before uploading new
            for document in existing_phrases.get('hits', []):
                doc_id = document.get('document', {}).get('id', '')
                if doc_id:
                    try:
                        client.collections[collection_name_tmp].documents[doc_id].delete()
                        print(f'Search phrase ID {doc_id} deleted for url {url}')
                    except typesense.exceptions.ObjectNotFound:
                        print(f'Search phrase ID {doc_id} not found in collection "{collection_name_tmp}"')

            upload_batch = []
            
            
            for index, phrase in enumerate(search_phrases):
                print(phrase)
                batch = {
                    'doc_id': search_hit.get('id',''),
                    'url': url,
                    'search_phrase': phrase.get('search_phrase', ''),
                    'sort_order': index,
                    'item_priority': 1,
                    'updated_at': int(datetime.datetime.utcnow().timestamp()),
                    'checksum': checksum_md,
                }
                upload_batch.append(batch)

            results = client.collections[collection_name_tmp].documents.import_(upload_batch, {'action': 'upsert', 'return_id': True})
            failed_results = [result for result in results if not result['success']]
            if len(failed_results) > 0:
                print(f'The following search_phrases for url:\n  \"{url}\"\n were not successfully upserted to typesense:\n{failed_results}')
            
            doc_index += 1
            # end while
            
        page += 1

    
    commit_tmp_collection(client, collection_name_tmp)

    return None


def commit_tmp_collection(client: typesense.Client, collection_name_tmp: str):
        """Update alias to point to new collection"""
        old_collection_name = None
        alias_name = env_var("TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION", '')

        try:
            old_collection_name = client.aliases[alias_name].retrieve()['collection_name']
        except typesense.exceptions.ObjectNotFound:
            pass

        client.aliases.upsert(alias_name, {'collection_name': collection_name_tmp})

        # if old_collection_name:
        #     client.collections[old_collection_name].delete()