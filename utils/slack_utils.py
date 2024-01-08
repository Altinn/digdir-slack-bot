from slack_sdk.errors import SlackApiError
import datetime
import pytz
from dataclasses import dataclass
from typing import Optional

@dataclass
class SlackContext:
    ts: str
    thread_ts: Optional[str]
    channel: str
    team: Optional[str]
    user: Optional[str]
    time_utc: Optional[str]


def get_event_context(msg_body) -> SlackContext:
    evt = msg_body.get('event')
    slack_context = SlackContext(
        ts=evt.get('ts'),
        thread_ts=evt.get('thread_ts'),
        channel=evt.get('channel'),
        team=evt.get('team'),
        user=evt.get('user'),
        time_utc= unixtime_to_timestamptz(msg_body.get("event_time", ""))
    )
    return slack_context

def get_context_from_thread_response(parent_ts, slack_response) -> SlackContext:
    slack_context = SlackContext(
        ts=slack_response.get('ts'),
        thread_ts=parent_ts,
        channel=slack_response.get('channel'),
        team=None,
        user=None,
        time_utc=None
    )
    return slack_context

def get_reaction_item_context(evt) -> SlackContext:
    item = evt.get('item', {})
    slack_context = SlackContext(
        ts=item.get('ts'),
        thread_ts=None,
        channel=item.get('channel'),
        team=None,
        user=None,
        time_utc=None
    )
    return slack_context

def unixtime_to_timestamptz(unixtime):
    if unixtime:
        event_time_utc = datetime.datetime.fromtimestamp(unixtime).astimezone(pytz.timezone('UTC'))                
        event_time_tz = event_time_utc.strftime("%Y-%m-%d %H:%M:%S")
        return event_time_tz
    
    return None

def time_s_to_ms(time_diff):
    return int(time_diff * 1000)

def is_user_admin(app, user_id):
    # Check if the current user is a Slack workspace admin
    try:
        user_info = app.client.users_info(user=user_id)
        is_admin = user_info["user"]["is_admin"]
    except SlackApiError as e:
        logger.error(f"Error fetching user info: {e}")
        is_admin = False

    if is_admin:
        print(f"User {user_id} is an admin.")
    else:
        print(f"User {user_id} is not an admin.")


def get_message(app, channel_id, message_ts):
    # ID of channel that the message exists in
    
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = app.client.conversations_history(
            channel=channel_id,
            inclusive=True,
            oldest=message_ts,
            limit=1
        )

        message = result["messages"][0]
        
        return message

    except SlackApiError as e:
        print(f"Error get_message(channel={channel_id}, message_ts={message_ts}): {e}")

    return None

def get_event_source_descriptor(msg_body):
    evt = msg_body.get("event")
    if not evt:
        return None
    
    return {
        "team": evt.get("team"),
        "channel": evt.get("channel"),
        "message": evt.get("ts"),
    }

# assumes msg.type = 'event'
def get_message_deeplink(msg_body):
    src = get_event_source_descriptor(msg_body)
    message_link = f'https://slack.com/app_redirect?team={src["team"]}&channel={src["channel"]}&message_ts={src["message"]}'    
    return message_link

def get_message_permalink(app, msg_body):
    src = get_event_source_descriptor(msg_body)
    
    return app.client.chat_getPermalink(channel=src["channel"], message_ts=src["message"]).get('permalink')

def register_custom_event(app, event_type):
    # Register a new event with Slack's Event API
    try:
        response = app.client.api_call(
            api_method='events.register',
            json={'type': event_type}
        )
        if response["ok"]:
            print(f"Event {event_type} registered successfully.")
        else:
            print(f"Failed to register event {event_type}. Error: {response['error']}")
    except SlackApiError as e:
        print(f"Error registering custom event: {e}")


def remove_message_attrib(msg_body, attrib_name):
    if 'message' in msg_body and attrib_name in msg_body['message']:
        del msg_body['message'][attrib_name]
    return msg_body
    