import os
import timeit
import typesense
import datetime

import docs_qa.typesense_search as search

from ragatouille import RAGPretrainedModel
from ragatouille.utils import get_wikipedia_page
from ragatouille.data import CorpusProcessor

from .config import config

cfg = config()


RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")


async def run():

    durations = {
        'query_docs': 0,
        'generate_phrases': 0,
        'store_phrases': 0,
        'total': 0
    }
    page = 1
    page_size = 100


    total_start = start = timeit.default_timer()

    fetch_start = timeit.default_timer()            

    all_docs = []

    while True:
      print(f'Retrieving content_markdown for all urls, page {page} (page_size={page_size})')

      search_response = await search.typesense_retrieve_all_urls(page, page_size)

      documents = [
          document['document'].get('content_markdown', '')
          for result in search_response['results']
          for hit in result['grouped_hits']
          for document in hit['hits']
      ]
      print(f'Retrieved {len(documents)} documents.')

      all_docs.extend(documents)


      if len(documents) == 0:
          print(f'Last page with results was page {page - 1}')
          break

      page += 1


    print(f'Fetch markdown content for {len(all_docs)} completed in {round(timeit.default_timer() - fetch_start, 1)}')

    start = timeit.default_timer()

    processor = CorpusProcessor()
    processed_corpus = processor.process_corpus(all_docs)
    index_path = RAG.index(index_name="docs-altinn-studio-colbert", collection=processed_corpus)

    print(f'ColBERT indexing completed in {round(timeit.default_timer() - start, 1)} seconds.\n  - Index path: {index_path}')


    return None