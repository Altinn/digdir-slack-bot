import box
import timeit
import yaml
import asyncio
import argparse
from dotenv import find_dotenv, load_dotenv
from code_qa.chain import setup_dbqa

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('code_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

async def code_query(user_input):
        # Setup DBQA
    dbqa = setup_dbqa()
    response = dbqa({'query': user_input})
    return response

def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(code_query(user_input))
    end = timeit.default_timer()

    print(f'\nAnswer: {response["result"]}')
    print('='*50)

    # Process source documents
    source_docs = response['source_documents']
    for i, doc in enumerate(source_docs):
        print(f'\nSource Document {i+1}\n')
        print(f'Source Text: {doc.page_content}')
        print(f'Document Name: {doc.metadata["source"]}')
        print(f'Metadata: {doc.metadata}')
        print('='* 60)

    print(f"Time to retrieve response: {end - start} seconds")
