'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
import box
import yaml
import os
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from dotenv import find_dotenv, load_dotenv
from utils.general import env_var

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def build_llm(streaming=False):

    
    if env_var('USE_AZURE_OPENAI_API') == True:
      llm = AzureChatOpenAI(
          deployment_name=env_var('AZURE_OPENAI_DEPLOYMENT'),
          azure_endpoint= env_var('AZURE_OPENAI_API_URL'),
          openai_api_key= env_var('AZURE_OPENAI_API_KEY'),
          openai_api_version= env_var('AZURE_OPENAI_VERSION'),
          temperature=cfg.TEMPERATURE, 
          max_tokens=cfg.MAX_NEW_TOKENS, 
          streaming=streaming)

    else:
       llm = ChatOpenAI(
          model= env_var('OPENAI_API_MODEL_NAME'),
          api_key= env_var('OPENAI_API_KEY'),
          temperature= cfg.TEMPERATURE,
          max_tokens= cfg.MAX_NEW_TOKENS,
          streaming= streaming
       )

    return llm
