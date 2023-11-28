import box
import yaml
import pprint
import typesense
from sentence_transformers import SentenceTransformer
from docs_qa.extract_search_terms import GeneratedSearchQueries

pp = pprint.PrettyPrinter(indent=2)

# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


async def typesense_search_multiple(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    print(f'incoming queries: {search_queries}')

    multi_search_args = {
        "searches":
            [
                {
                    "collection":"altinn-studio-docs",                
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
                    "collection":"altinn-studio-docs-search-phrases",      
                     "q": query,
                    "query_by": "search_phrase,phrase_vec",
                    "include_fields": "url",
                    "group_by":"url",
                    "group_limit":5,
                    "limit": 30,
                    "sort_by": "_text_match:desc",
                    "prioritize_exact_match": True,
                    "drop_tokens_threshold": 5,                                    
                }
                for query in search_queries.searchQueries
            ]
        }
    # print(f'multi_search_args:')
    # pprint.pprint(multi_search_args)
    response = client.multi_search.perform(multi_search_args, {})
    return response

async def typesense_search_multiple_vector(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    print(f'incoming queries, converting to vectors:\n{search_queries}')

    # Convert search queries to vectors using all-MiniLM-L12-v2
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    vector_queries = [model.encode(query) for query in search_queries.searchQueries]
    
    multi_search_args = {
        "searches":
            [
                {
                    "collection":"altinn-studio-docs",                
                    "q": "*",
                    "vector_query": f"embedding:([{','.join(str(v) for v in query)}], k:10)",
                    "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id,content_markdown",
                }
                for query in vector_queries
            ]
        }
    print(f'multi_search_args:')
    pprint.pprint(multi_search_args)

    response = client.multi_search.perform(multi_search_args, {})
    return response

async def typesense_retrieve_all_urls(page, page_size):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    multi_search_args = {
        "searches":
            [
                {
                    "collection":"altinn-studio-docs",                
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
    
    print(f'multi_search_args:')
    pprint.pprint(multi_search_args)

    response = client.multi_search.perform(multi_search_args, {})
    return response


async def typesense_retrieve_all_by_url(url_list):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    url_searchs = [
        {
            "collection":"altinn-studio-docs",                
            "q": url,
            "query_by":"url_without_anchor",
            "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id,content_markdown",
            "group_by":"url_without_anchor",
            "group_limit": 1,
            "page": 1,
            "per_page": 1
        } 
        for url in url_list
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
            'token_separators': ['_', '-']
        }
    
    try:
        client.collections[collection_name_tmp].retrieve()
    except typesense.exceptions.ObjectNotFound:
        client.collections.create(schema)
    
async def lookup_search_phrases(url):
    """Get existing search phrases for url"""

    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    multi_search_args = {
        "searches":
            [
                {
                    "collection":"altinn-studio-docs-search-phrases",                
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