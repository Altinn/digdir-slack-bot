import os
import openai
import instructor
from pydantic import BaseModel, Field
import pprint


instructor.patch()
openai.api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']

class ExtractedSearchTerms(BaseModel):
    searchTerms: list[str] = Field(description="Array of search terms.")

pp = pprint.PrettyPrinter(indent=2)

async def run_query_async(user_input):
    
    print(f"user_input: {user_input}")

    query_result: ExtractedSearchTerms = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        response_model=ExtractedSearchTerms,
        messages=[
            {"role": "system", "content": "Analyze the following support request and extract the most important words to use in a text search:"},
            {"role": "user", "content": user_input},
        ]
    )

    print("Response:")
    pp.pprint(query_result)

    return query_result