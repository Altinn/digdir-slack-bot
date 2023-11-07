import os
import dataclasses
from supabase import create_client, Client
from utils.slack_utils import SlackContext


@dataclasses.dataclass
class BotLogEntry:
    slack_context: SlackContext
    elapsed_ms: int
    step_name: str
    payload: object = None
    rag_llm_feedback: object = None
    durations: object = None

# create single supabase client
supabase: Client = create_client(os.environ['SLACK_BOT_SUPABASE_URL'],
                                 os.environ['SLACK_BOT_SUPABASE_API_KEY'])


def bot_log(entry: BotLogEntry):

    insert_response = supabase.table('bot_log').insert(dataclasses.asdict(entry)).execute()
    
    print(f'insert_response: {insert_response}')
    return insert_response
