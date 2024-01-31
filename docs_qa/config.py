import box
import yaml
import pprint
from utils.general import env_var

pp = pprint.PrettyPrinter(indent=2)

def config():
    
    # Import config vars
    with open('docs_qa/config/config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
        cfg.TYPESENSE_CONFIG.api_key = env_var("TYPESENSE_API_KEY")
        cfg.TYPESENSE_CONFIG.nodes[0].host = env_var("TYPESENSE_API_HOST")

    if not env_var("TYPESENSE_DOCS_COLLECTION"):
        raise Exception("Environment variable 'TYPESENSE_DOCS_COLLECTION' is not set.")
    if not env_var("TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION"):
        raise Exception("Environment variable 'TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION' is not set.")

    return cfg

