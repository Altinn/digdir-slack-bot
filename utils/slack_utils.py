from slack_sdk.errors import SlackApiError

def get_message_metadata(msg_body):

    source_msg_meta = {
        'ts': msg_body.get('event').get('ts'),
        'channel': msg_body.get('event').get('channel'),
        'team': msg_body.get('event').get('team'),
        'user': msg_body.get('event').get('user')                
    }

    return source_msg_meta


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
    