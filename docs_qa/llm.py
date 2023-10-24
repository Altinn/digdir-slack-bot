'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
import box
import yaml
import os
from langchain.llms import CTransformers
from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def build_llm():
    if cfg.MODEL_TYPE.startswith('gpt-'):
        api_key = os.environ['OPENAI_API_KEY_ALTINN3_DEV']
        llm = ChatOpenAI(model_name=cfg.MODEL_TYPE, 
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
