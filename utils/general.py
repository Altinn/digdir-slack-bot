import os
from urllib.parse import urlparse


def env_full_name(var_name):
    return os.getenv('DIGDIR_SLACK_BOT_PREFIX', '') + var_name + os.getenv('DIGDIR_SLACK_BOT_POSTFIX', '')

def env_var(var_name, default=None):
    return os.getenv(env_full_name(var_name), default)

def env_var_with_scope(var_name, scope_name, default=None):
    r = None
    if scope_name:
        r = os.getenv(f'{scope_name}_{var_name}')

    if not scope_name or r == None:
        r = os.getenv(var_name, default)
    
    return r

def scoped_env_var(scope_name):
    def inner(var_name, default=None):
        return env_var_with_scope(var_name, scope_name, default)
    return inner


def is_valid_url(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except ValueError:
      return False
