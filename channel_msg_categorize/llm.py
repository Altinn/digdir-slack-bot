'''
===========================================
        Module: LLM Setup
===========================================
'''
import os
import pprint
from dotenv import find_dotenv, load_dotenv

import openai
from langchain.llms import CTransformers
from langchain.chat_models import AzureChatOpenAI

from .config_chain import config


pp = pprint.PrettyPrinter(indent=2)

# Load environment variables from .env file
load_dotenv(find_dotenv())
cfg = config()

openai.api_type = 'azure'
openai.api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']
openai.api_base = os.environ['OPENAI_API_URL_ALTINN3_DEV']
openai.api_version = os.environ['AZURE_OPENAI_VERSION']


def build_llm():

  llm = AzureChatOpenAI(
              engine=cfg.MODEL_TYPE, 
              deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT'],
              temperature=cfg.TEMPERATURE, 
              max_tokens=cfg.MAX_NEW_TOKENS)



  print(f'LLM config:\n')
  pp.pprint(llm)

  return llm
