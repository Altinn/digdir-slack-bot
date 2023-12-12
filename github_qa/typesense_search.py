import os
import box
import yaml
import pprint
import typesense
from docs_qa.extract_search_terms import GeneratedSearchQueries
from .config import config 


pp = pprint.PrettyPrinter(indent=2)
cfg = config()

async def typesense_search_multiple(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    print(f'incoming queries: {search_queries}')

    multi_search_args = {
        "searches":
            [
                {
                    "collection":"gh-studio-issues",                
                    "q": query,
                    "query_by":"title,body,body_embedding",
                    "include_fields":"title,body,id,url,labels,state",
                    "limit": 12,
                    "prioritize_exact_match": False,
                    # "sort_by": "_text_match:desc", # should default to vector_distance
                    "drop_tokens_threshold": 8,                
                    "pre_segmented_query": True,
                    "exhaustive_search": True,                    
                    "highlight_affix_num_tokens":4
                }
                for query in search_queries.searchQueries
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)
    response = client.multi_search.perform(multi_search_args, {})
    return response

