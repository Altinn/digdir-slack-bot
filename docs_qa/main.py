import box
import timeit
import yaml
import asyncio
import argparse
import typesense
import pprint
from dotenv import find_dotenv, load_dotenv
from docs_qa.chain import setup_dbqa
from docs_qa.extract_search_terms import run_query_async

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

async def call_typesense(search_terms):
    client = typesense.Client({
        'nodes': [{
            'host': 'altinn-typesense-api.azurewebsites.net',
            'port': '443',
            'protocol': 'https'
        }],
        'api_key': 'xyx',
        'connection_timeout_seconds': 2
    })

    multi_search_args = {
        'q': (" ".join(search_terms)), 'query_by': 'content', 'sort_by': '_text_match:desc'
    }

    response = client.collections['altinn-studio-docs'].documents.search(multi_search_args)
    return response



def main(user_input):

    start = timeit.default_timer()
    # response = asyncio.run(docs_query(user_input))
    extract_search_terms = asyncio.run(run_query_async(user_input))
    pp.pprint(extract_search_terms)
    search_response = asyncio.run(call_typesense(extract_search_terms.searchTerms))
    pp.pprint(search_response)

    # todo: 
    #   parse search result list, extracting document IDs
    #   retrieve embeddings from typesense for all documents
    #   query GPT with embeddings



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
