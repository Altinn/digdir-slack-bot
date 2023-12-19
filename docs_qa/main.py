import timeit
import asyncio
import pprint

from rag_with_typesense import rag_with_typesense


pp = pprint.PrettyPrinter(indent=2)

def main(user_input):

    start = timeit.default_timer()
    response = asyncio.run(rag_with_typesense(user_input))

    # print('stuff chain response:')
    # pp.pprint(response)

    end = timeit.default_timer()

    # print(f'\nAnswer: {response["result"]}')
    # print('='*50)

    # # Process source documents
    # source_docs = response['source_documents']
    # for i, doc in enumerate(source_docs):
    #     print(f'\nSource Document {i+1}\n')
    #     print(f'Source Text: {doc.page_content}')
    #     print(f'Document Name: {doc['metadata']["source"]}')
    #     print(f'Metadata: {doc.metadata}')
    #     print('='* 60)

    print(f"Time to retrieve response: {end - start} seconds")
