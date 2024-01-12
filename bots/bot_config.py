import os
import dataclasses
from supabase import create_client, Client
from .utils.slack_utils import SlackContext


# create single supabase client
supabase: Client = create_client(os.environ['SLACK_BOT_SUPABASE_URL'],
                                 os.environ['SLACK_BOT_SUPABASE_API_KEY'])


def bot_config(slack_context : SlackContext):
    table_name = supabase.table('bot_config')  
    channel_id = "C06AU0HDF9B" #slack_context.channel
    data = supabase.table(table_name).select("*").execute()

# Check if the fetch was successful
    if data.error:
        print(f"An error occurred: {data.error}")
    else:
    # Loop through the rows
        for row in data.data:
        # Process each row (as a dictionary)
            if channel_id ==  row.get('channel_id') :
                col_config = row.get('config') 
                print(col_config)
                return col_config 
    
    return {}
                
                 
