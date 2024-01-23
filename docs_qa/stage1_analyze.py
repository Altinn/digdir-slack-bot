'''
===========================================
        Module: Analyze user input
===========================================
'''
import os
from openai import AzureOpenAI
import instructor
from pydantic import BaseModel, Field

from .prompts import stage1_analyze_query
from .config import config

cfg = config()

class UserQueryAnalysis(BaseModel):
    userInputLanguageCode: str = Field(..., description="ISO 639-1 language code for the user query")
    userInputLanguageName: str = Field(..., description="ISO 639-1 language name for the user query")
    questionTranslatedToEnglish: str = Field(..., description="The user's question, translated to English")
    contentCategory: str = Field(..., description="One of the following categories: [Support Request], [For Your Information], [Pull request announcement], [None of the above]")

llmClient = instructor.patch(AzureOpenAI(
    azure_endpoint = os.environ['OPENAI_API_URL_ALTINN3_DEV'],
    api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV'],
    api_version = os.environ['AZURE_OPENAI_VERSION']
))
    

async def query(user_input) -> UserQueryAnalysis:
    query_result: UserQueryAnalysis = llmClient.chat.completions.create(
        model=os.environ['AZURE_OPENAI_DEPLOYMENT'],
        response_model=UserQueryAnalysis,
        temperature=0.1,
        max_retries=0,
        messages=[
            {"role": "system", "content": stage1_analyze_query},
            {"role": "user", "content": user_input},
        ],
        
    )
    return query_result