'''
===========================================
        Module: LLM Setup
===========================================
'''
import os
import pprint

from langchain.chat_models import AzureChatOpenAI


pp = pprint.PrettyPrinter(indent=2)


def build_llm():

  llm = AzureChatOpenAI(
          deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT'],
          azure_endpoint= os.environ['OPENAI_API_URL_ALTINN3_DEV'],
          openai_api_key= os.environ['OPENAI_API_KEY_ALTINN3_DEV'],
          openai_api_version= os.environ['AZURE_OPENAI_VERSION'])


  print(f'LLM config:\n')
  pp.pprint(llm)

  return llm
