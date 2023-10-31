import os
from supabase_py import create_client, Client
from box import Box
import dataclasses
from typing import Any, Dict
from utils.slack_utils import SlackContext


@dataclasses.dataclass
class BotLogEntry:
    slack_context: SlackContext
    elapsed_ms: int
    step_name: str
    payload: object

# create single supabase client
supabase: Client = create_client(os.environ['SLACK_BOT_SUPABASE_URL'],
                                 os.environ['SLACK_BOT_SUPABASE_API_KEY'])


def bot_log(entry: BotLogEntry):
    # Convert the BotLogEntry object to a dictionary
    # entry_dict = entry.__dict__
    # Convert the dictionary to a JSON string
    # entry_json = json.dumps(entry_dict)
    insert_response = supabase.table('bot_log').insert(dataclasses.asdict(entry)).execute()

    print(f'insert_response: {insert_response}')
    return insert_response
