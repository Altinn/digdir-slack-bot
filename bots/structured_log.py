import box
import yaml
import os
from supabase_py import create_client, Client
from box import Box
from dataclasses import dataclass
import json
from typing import Any, Dict


@dataclass
class BotLogEntry:
    slack_ts: str
    thread_ts: str
    slack_user_id: str
    slack_msg_time: int
    elapsed_ms: int
    step_name: str
    payload: object

# create single supabase client
supabase: Client = create_client(os.environ['SLACK_BOT_SUPABASE_URL'],
                                 os.environ['SLACK_BOT_SUPABASE_API_KEY'])


def bot_log(entry: BotLogEntry):
    # Convert the BotLogEntry object to a dictionary
    entry_dict = entry.__dict__
    # Convert the dictionary to a JSON string
    # entry_json = json.dumps(entry_dict)
    insert_response = supabase.table('bot_log').insert(entry_dict).execute()

    print(f'insert_response: {insert_response}')
    return insert_response
