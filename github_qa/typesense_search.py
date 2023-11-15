import box
import yaml
import pprint
import typesense
from docs_qa.extract_search_terms import GeneratedSearchQueries

pp = pprint.PrettyPrinter(indent=2)

# Import config vars
with open('github_qa/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


async def typesense_search_multiple(search_queries: GeneratedSearchQueries):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    print(f'incoming queries: {search_queries}')

    multi_search_args = {
        "searches":
            [
                {
                    "collection":"gh-studio-issues",                
                    "q": query,
                    "query_by":"title,body",
                    "include_fields":"title,body,id,url",
                    "limit": 20,
                    "prioritize_exact_match": False,
                    "sort_by": "_text_match:desc",
                    "drop_tokens_threshold": 8,                
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

