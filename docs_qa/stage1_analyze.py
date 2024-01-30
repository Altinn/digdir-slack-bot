'''
===========================================
        Module: Analyze user input
===========================================
'''
import os
from pydantic import BaseModel, Field

from .prompts import stage1_analyze_query
from utils.general import scoped_env_var
from .config import config, azure_client, openai_client

stage_name = 'DOCS_QA_ANALYZE'
env_var = scoped_env_var(stage_name)


cfg = config()
azureClient = azure_client()
openaiClient = openai_client()


class UserQueryAnalysis(BaseModel):
    userInputLanguageCode: str = Field(..., description="ISO 639-1 language code for the user query")
    userInputLanguageName: str = Field(..., description="ISO 639-1 language name for the user query")
    questionTranslatedToEnglish: str = Field(..., description="The user's question, translated to English")
    contentCategory: str = Field(..., description="One of the following categories: [Support Request], [For Your Information], [Pull request announcement], [None of the above]")

    
async def query(user_input) -> UserQueryAnalysis:
    query_result: UserQueryAnalysis

    if env_var('USE_AZURE_OPENAI_API') == True:
        query_result = azureClient.chat.completions.create(
            model= env_var('AZURE_OPENAI_DEPLOYMENT'),
            response_model=UserQueryAnalysis,
            temperature=0.1,
            max_retries=0,
            messages=[
                {"role": "system", "content": stage1_analyze_query},
                {"role": "user", "content": user_input},
            ])    
    else:
        print(f"{stage_name} model name: {env_var('OPENAI_API_MODEL_NAME')}")
        query_result = openaiClient.chat.completions.create(
            model= env_var('OPENAI_API_MODEL_NAME'), 
            response_model=UserQueryAnalysis,
            temperature=0.1,
            max_retries=0,
            messages=[
                {"role": "system", "content": stage1_analyze_query},
                {"role": "user", "content": user_input},
            ])

    return query_result