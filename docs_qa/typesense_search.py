import pprint
import typesense
# from sentence_transformers import SentenceTransformer
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
                    "collection": cfg.DOCS_COLLECTION,
                    "q": query,
                    "query_by":"content,embedding",
                    "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id,content_markdown",
                    "group_by":"url_without_anchor",
                    "group_limit":3,
                    "limit": 10,
                    "prioritize_exact_match": False,
                    "sort_by": "_text_match:desc",
                    "drop_tokens_threshold": 5,                                    
                }
                for query in search_queries.searchQueries
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)
    response = client.multi_search.perform(multi_search_args, {})
    return response


async def lookup_search_phrases_similar(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    multi_search_args = {
        "searches":
            [
                {
                    "collection": cfg.DOCS_SEARCH_PHRASE_COLLECTION,
                    "q": query,
                    "query_by": "search_phrase,phrase_vec",
                    "include_fields": "search_phrase,url",
                    "group_by": "url",
                    "group_limit": 1,
                    "limit": 20,
                    "sort_by": "_text_match:desc,_vector_distance:asc",
                    "prioritize_exact_match": False,
                    "drop_tokens_threshold": 5,                                    
                }
                for query in search_queries.searchQueries
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)
    response = client.multi_search.perform(multi_search_args, {})

    # print(f'lookup_search_phrases_similar raw response:')
    # pp.pprint(response)


    search_phrase_hits = [
        phrase
        for result in response['results']
        for hit in result['grouped_hits']
        for phrase in hit['hits']
        # for phrase in result['hits']
    ]
    search_phrase_hits.sort(key=lambda x: x['hybrid_search_info']['rank_fusion_score'], reverse=True)

    print(f'Sorted search phrase result list:')
    pp.pprint(search_phrase_hits)

    url_list = [
        {
            'url': phrase['document']['url'],
            'rank': phrase['hybrid_search_info']['rank_fusion_score'],
        }
        for phrase in search_phrase_hits
    ]
    unique_urls = []
    for url in url_list:
        if url['url'] not in [u['url'] for u in unique_urls]:
            unique_urls.append(url)


    # for url in url_list:
    #     if url not in [u['url'] for u in unique_urls]:
    #         unique_urls.append(url)
    
    return unique_urls

async def typesense_search_multiple_vector(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

#     print(f'incoming queries, converting to vectors:\n{search_queries}')

#     # Convert search queries to vectors using all-MiniLM-L12-v2
#     model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

#     vector_queries = [model.encode(query) for query in search_queries.searchQueries]
    
    multi_search_args = {
        "searches":
            [
                {
                    "collection": cfg.DOCS_COLLECTION,
                    "q": "*",
                    "vector_query": f"embedding:([{','.join(str(v) for v in query)}], k:10)",
                    "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id,content_markdown",
                }
                for query in vector_queries
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)

    response = client.multi_search.perform(multi_search_args, {})
    return response

async def typesense_retrieve_all_urls(page, page_size):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    multi_search_args = {
        "searches":
            [
                {
                    "collection": cfg.DOCS_COLLECTION,                
                    "q": "*",
                    "query_by":"url_without_anchor",
                    "include_fields":"url_without_anchor,content_markdown,id",
                    "group_by":"url_without_anchor",
                    "group_limit":1,
                    "sort_by": "item_priority:asc",
                    "page": page,
                    "per_page": page_size,
                }
            ]
        }
    
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)

    response = client.multi_search.perform(multi_search_args, {})
    return response


async def typesense_retrieve_all_by_url(url_list):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    url_searchs = [
        {
            "collection": cfg.DOCS_COLLECTION,             
            "q": ranked_url['url'],
            "query_by":"url_without_anchor",
            "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id,content_markdown",
            "filter_by": f"url_without_anchor:={ranked_url['url']}",
            "group_by":"url_without_anchor",
            "group_limit": 1,
            "page": 1,
            "per_page": 1
        } 
        for ranked_url in url_list[:20]
    ]
    # pp.pprint(url_searchs)

    multi_search_args = { "searches": url_searchs }

    response = client.multi_search.perform(multi_search_args, {})
    return response

def setup_search_phrase_schema(collection_name_tmp):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)    
    schema = {
            'name': collection_name_tmp,
            'fields': [
                {'name': 'doc_id', 'type': 'string', 'optional': False},
                {'name': 'url', 'type': 'string', 'optional': False, 'facet': True, 'sort': True},
                {'name': 'search_phrase', 'type': 'string', 'optional': False},
                {'name': 'sort_order', 'type': 'int32', 'optional': False, 'sort': True},
                {'name': 'phrase_vec', 'type': 'float[]', 'optional': True, 
                 'embed': { 'from': ['search_phrase'], 
                            'model_config': {
                                'model_name': 'ts/all-MiniLM-L12-v2'
                            }}},
                {'name': 'language', 'type': 'string', 'facet': True, 'optional': True},
                {'name': 'item_priority', 'type': 'int64'},
            ],
            'default_sorting_field': 'sort_order',
            'token_separators': ['_', '-', '/']
        }
    
    try:
        client.collections[collection_name_tmp].retrieve()
    except typesense.exceptions.ObjectNotFound:
        client.collections.create(schema)
    
async def lookup_search_phrases(url, collection_name: str):
    """Get existing search phrases for url"""

    client = typesense.Client(cfg.TYPESENSE_CONFIG)
    if collection_name == None:
        collection_name = cfg.DOCS_SEARCH_PHRASE_COLLECTION

    multi_search_args = {
        "searches":
            [
                {
                    "collection": collection_name,
                    "q": "*",
                    "query_by":"url",
                    "include_fields": "id,url,search_phrase,sort_order",
                    "filter_by": f"url:={url}",
                    "sort_by": "sort_order:asc",                
                    "per_page": 30,
                }                
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)
    response = client.multi_search.perform(multi_search_args, {})
    return response