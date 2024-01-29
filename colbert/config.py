import os
import box
import yaml
import pprint



pp = pprint.PrettyPrinter(indent=2)

def env_var(var_name):
    full_var_name = os.environ.get('DIGDIR_SLACK_BOT_PREFIX') + var_name + os.environ.get('DIGDIR_SLACK_BOT_POSTFIX')
    return os.environ[full_var_name]

def config():
    
    # Import config vars
    with open('colbert/config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
        cfg.TYPESENSE_CONFIG.api_key = os.environ["TYPESENSE_API_KEY_ALTINN3_DEV"]
        cfg.TYPESENSE_CONFIG.nodes[0].host = os.environ["TYPESENSE_API_HOST_ALTINN3_DEV"] 

    if not os.environ.get("TYPESENSE_DOCS_COLLECTION", None):
        raise Exception("Environment variable 'TYPESENSE_DOCS_COLLECTION' is not set.")
    if not os.environ.get("TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION", None):
        raise Exception("Environment variable 'TYPESENSE_DOCS_SEARCH_PHRASE_COLLECTION' is not set.")

    return cfg
