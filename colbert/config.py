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

    return cfg
