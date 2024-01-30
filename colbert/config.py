import box
import yaml
import pprint


pp = pprint.PrettyPrinter(indent=2)

def config():
    
    # Import config vars
    with open('colbert/config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    return cfg
