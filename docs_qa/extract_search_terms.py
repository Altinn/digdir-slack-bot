import box
import yaml
import os
import openai
import instructor
from pydantic import BaseModel, Field
import pprint


# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


instructor.patch()
openai.api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']

class GeneratedSearchQueries(BaseModel):
    searchQueries: list[str] = Field(description="Array of search queries.")

pp = pprint.PrettyPrinter(indent=2)


async def run_query_async(user_input) -> GeneratedSearchQueries:    
    query_result: GeneratedSearchQueries = openai.ChatCompletion.create(
        model=cfg.MODEL_TYPE,
        response_model=GeneratedSearchQueries,
        messages=[
            {"role": "system", 
             "content": f"""You have access to a search API that returns relevant documentation.
Generate an array of search queries that are relevant to this question.
Use a variation of related keywords for the queries, trying to be as general as possible.
Include as many queries as you can think of, including and excluding terms.
For example, include queries like ['keyword_1 keyword_2', 'keyword_1', 'keyword_2'].
Be creative. The more queries you include, the more likely you are to find relevant results."""},
            {"role": "user", "content": user_input},
        ]
    )
    return query_result