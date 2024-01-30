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
from utils.general import env_var

# Load environment variables from .env file
load_dotenv(find_dotenv())


cfg = config()

def build_llm():
    
    if cfg.MODEL_TYPE == 'gpt-4':
        api_key = env_var('OPENAI_API_KEY')
        endpoint = env_var('OPENAI_API_URL')
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
