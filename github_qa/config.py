import os
import box
import yaml
import pprint
from utils.general import env_var

pp = pprint.PrettyPrinter(indent=2)


def config():
    
    # Import config vars
    with open('github_qa/config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
        cfg.TYPESENSE_CONFIG.api_key = env_var("TYPESENSE_API_KEY")
        cfg.TYPESENSE_CONFIG.nodes[0].host = env_var("TYPESENSE_API_HOST") 

    return cfg

