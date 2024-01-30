import os
import timeit
from supabase import create_client, Client
from utils.slack_utils import SlackContext
from utils.general import env_var

# create single supabase client
supabase: Client = create_client(env_var('SLACK_BOT_SUPABASE_URL'),
                                 env_var('SLACK_BOT_SUPABASE_API_KEY'))


def lookup_config(slack_context : SlackContext, config_name: str, default_value):
    
    channel_id = slack_context.channel

    start = timeit.default_timer()
    try:
        (data, count) = supabase.table('bot_config').select("*").execute()
    except Exception as supabase_ex:
        print(f'Supabase error occurred when attempting to log:\n{supabase_ex}')
        return default_value
    
    duration = round(timeit.default_timer() - start, 1)
    if duration > 0.1:
        print(f'Took {duration} seconds to lookup config from db.')

    for row in data[1]:

        if channel_id == row.get('channel_id'):
            col_config = row.get('config') 
            config_value = col_config.get(config_name, default_value)
            print(f'Found config matching channel_id {channel_id} - config:\n{col_config}\n\nProperty {config_name} = {config_value}\n')
            
            return config_value
    
    # didn't find matching config
    return default_value
                
                 
