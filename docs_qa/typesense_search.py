import box
import yaml
import pprint
import typesense
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
                    "query_by":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,hierarchy.lvl5,hierarchy.lvl6,content,content_embedding",
                    "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,url_without_anchor,type,id",
                    "group_by":"url_without_anchor",
                    "group_limit":3,
                    "limit": 10,
                    "prioritize_exact_match": False,
                    "sort_by": "_text_match:desc",
                    "drop_tokens_threshold": 5,                
                    "pre_segmented_query": True,
                    # "snippet_threshold":8,
                    "highlight_affix_num_tokens":4
                }
                for query in search_queries.searchQueries
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
            "collection":"altinn-studio-docs",                
            "q": url,
            "query_by":"url_without_anchor",
            "include_fields":"hierarchy.lvl0,hierarchy.lvl1,hierarchy.lvl2,hierarchy.lvl3,hierarchy.lvl4,hierarchy.lvl5,hierarchy.lvl6,content,anchor,url,url_without_anchor,type,id",
            "group_by":"url_without_anchor",
            "filter_by": "type:=content",
            # "sort_by":"item_priority:desc",
            # "snippet_threshold":8,
            "per_page": 30
        } 
        for url in url_list
    ]
    # pp.pprint(url_searchs)

    if len(url_searchs) > 1:
        url_searchs = url_searchs[:1]
    multi_search_args = { "searches": url_searchs }

    response = client.multi_search.perform(multi_search_args, {})
    return response

