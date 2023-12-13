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

    try:
        insert_response = supabase.table('bot_log').insert(dataclasses.asdict(entry)).execute()
    except Exception as supabase_ex:
        print(f'Supabase error occurred when attempting to log:\n{supabase_ex}')
        return None

    print(f'insert_response: {insert_response}')
    return insert_response


def update_reactions(slack_context: SlackContext, reactions: object):
    
    ts = slack_context.ts
    channel = slack_context.channel
    # retrieve the correct row, looking for slack_context.ts in the slack_context column, which is jsonb type
    result_set = supabase.table('bot_log').select("*").eq("slack_context->>ts", ts).eq("slack_context->>channel", channel).execute()
    if result_set and len(result_set.data) > 0:
        # update the row, storing the reactions object in the field called 'reactions'
        update_response = supabase.table('bot_log').update({'reactions': reactions}).eq("id", result_set.data[0].get("id")).execute()
        print(f'update_response: {update_response}')

    return result_set
