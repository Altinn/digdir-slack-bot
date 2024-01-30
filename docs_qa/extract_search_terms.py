from pydantic import BaseModel, Field
import pprint
from .config import config, env_var, azure_client, openai_client

cfg = config()
azureClient = azure_client()
openaiClient = openai_client()

pp = pprint.PrettyPrinter(indent=2)


class GeneratedSearchQueries(BaseModel):
    searchQueries: list[str] = Field(..., description="Array of search queries.")


# alternative formulation: 
# 1. Generate the shortest set of search terms that sufficiently limits the set of expected query results.


async def run_query_async(user_input) -> GeneratedSearchQueries:    
    query_result: GeneratedSearchQueries 
    
    if env_var('USE_AZURE_OPENAI_API') == True:
        query_result = azureClient.chat.completions.create(
            model=env_var('AZURE_OPENAI_DEPLOYMENT'),
            response_model=GeneratedSearchQueries,
            temperature=0.1,
            max_retries=0,
            messages=[
                {"role": "system", 
                "content": f"""You have access to a search API that returns relevant documentation.

Your task is to generate an array of up to 7 search queries that are relevant to this question. 
Use a variation of related keywords and synonyms for the queries, trying to be as general as possible.
Include as many queries as you can think of, including and excluding terms.
For example, include queries like ['keyword_1 keyword_2', 'keyword_1', 'keyword_2'].
Be creative. The more queries you include, the more likely you are to find relevant results."""},
                {"role": "user", "content": "[User query]\n" + user_input},
            ]
        )
    else:
        query_result = openaiClient.chat.completions.create(
            model=env_var('OPENAI_API_MODEL_NAME'),
            response_model=GeneratedSearchQueries,
            temperature=0.1,
            max_retries=0,
            messages=[
                {"role": "system", 
                "content": f"""You have access to a search API that returns relevant documentation.

Your task is to generate an array of up to 7 search queries that are relevant to this question. 
Use a variation of related keywords and synonyms for the queries, trying to be as general as possible.
Include as many queries as you can think of, including and excluding terms.
For example, include queries like ['keyword_1 keyword_2', 'keyword_1', 'keyword_2'].
Be creative. The more queries you include, the more likely you are to find relevant results."""},
                {"role": "user", "content": "[User query]\n" + user_input},
            ]
        )

    for i in range(len(query_result.searchQueries)):
        query_result.searchQueries[i] = query_result.searchQueries[i].replace("GitHub", "").strip()
        

    return query_result