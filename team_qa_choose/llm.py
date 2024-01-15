'''
===========================================
        Module: LLM Setup
===========================================
'''
import os
from dotenv import find_dotenv, load_dotenv

from langchain_community.llms import CTransformers
from langchain_openai import ChatOpenAI

from .config_chain import config

# Load environment variables from .env file
load_dotenv(find_dotenv())


cfg = config()

def build_llm():
    
    if cfg.MODEL_TYPE == 'gpt-4':
        api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']
        endpoint = os.environ['OPENAI_API_URL_ALTINN3_DEV']
        llm = ChatOpenAI(model_name=cfg.MODEL_TYPE,                          
                         openai_api_base=endpoint,
                         temperature=cfg.TEMPERATURE, max_tokens=cfg.MAX_NEW_TOKENS,
                         openai_api_key=api_key)

    else:
        # Local CTransformers model
        llm = CTransformers(model=cfg.MODEL_BIN_PATH,
                                model_type=cfg.MODEL_TYPE,
                                config={'max_new_tokens': cfg.MAX_NEW_TOKENS,
                                        'temperature': cfg.TEMPERATURE}
                                )

    return llm
