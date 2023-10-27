"""
===========================================
        Module: Slack bot Bolt app
===========================================
"""
import os
import box
import yaml
import asyncio
import pprint
import copy


from slack_bolt import App
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

import utils.slack_utils as slack_utils
from bots.choose_team import run_bot_async as bot_choose_team
from bots.code_qa import run_bot_async as bot_code_qa
from bots.docs_qa import run_bot_async as bot_docs_qa

# Import config vars
with open("bolt-config.yml", "r", encoding="utf8") as ymlfile:
    boltcfg = box.Box(yaml.safe_load(ymlfile))

slack_bot_suffix = boltcfg.SLACK_BOT_SUFFIX

# Install the Slack app and get xoxb- token in advance
app = App(
    token=os.environ["SLACK_BOT_TOKEN" + slack_bot_suffix],
    signing_secret=os.environ["SLACK_BOT_SIGNING_SECRET" + slack_bot_suffix],
)

bot_query_word_code = "[code] "
bot_query_word_docs = "[docs] "
bot_query_word_team = "[team] "

pp = pprint.PrettyPrinter(indent=2)

hitl_config = {
    'enabled': True,
    'qa_channel': os.environ["SLACK_BOT_REVIEW_CHANNEL_ID"]
}

@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")


@app.event("app_mention")
def event_test(say):
    say("Hi there!")


@app.event("message")
def handle_message_events(ack, say, body, logger):
    print(f"-- incoming slack message event payload --")
    pp.pprint(body)

    evt = body["event"]
    if evt.get("type") == "message":
        if evt.get("subtype") == "message_deleted":
            logger.info(f"Ignoring message_deleted event.")

        text = evt.get("text", "")
        print(f"user input: {text}")
        if not evt.get("thread_ts"):
            # message is not in a thread

            if text.startswith(bot_query_word_docs):
                asyncio.run(
                    bot_docs_qa(app, hitl_config, say, body, text.replace(bot_query_word_docs, ""))
                )
            elif text.startswith(bot_query_word_code):
                asyncio.run(
                    bot_code_qa(app, hitl_config, say, body, text.replace(bot_query_word_code, ""))
                )
            elif text.startswith(bot_query_word_team):
                asyncio.run(
                    bot_choose_team(
                        app, hitl_config, say, body, text.replace(bot_query_word_team, "")
                    )
                )
            elif not text.startswith('['):
                asyncio.run(
                    bot_docs_qa(app, hitl_config, say, body, text)
                )
            else:
                print(f"Unknown query type: '{text}'")


@app.action("approve_button")
def update_message(ack):
    ack()
    print(f"approve button pressed")


@app.event("reaction_added")
def handle_reaction_added(event, say):
    print(f"Reaction added event: ")
    pp.pprint(event)


@app.event("reaction_removed")
def handle_reaction_removed(event, say):
    print(f"Reaction removed event: ")
    pp.pprint(event)


@app.action("[team][choose][confirm]")
def handle_team_choose_confirm(ack, body, logger):
    print(f"ack - action_id:'[team][choose][confirm]'")
    # Acknowledge the interaction
    ack()

    # Log the body of the interaction payload
    pp.pprint(body)
    # logger.info(body)

    user_id = body["user"]["id"]

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

    # Send a reply to the thread confirming that the message action was successful
    try:
        app.client.chat_postMessage(
            channel=body["channel"]["id"],
            thread_ts=body["message"]["ts"],
            user_id=user_id,
            text=f"<@{user_id}> gave the thumbs-up.\nI'll send this reply to <source workspace>-<thread_ts>",
        )

    except SlackApiError as e:
        logger.error(f"Error sending confirmation: {e}")

@app.action("docs|qa|approve_reply")
def handle_action_docs_qa_approve_reply(ack, body, logger):
    
    action = next((action for action in body.get('actions', []) if action.get('action_id') == 'docs|qa|approve_reply'), None)

    if action is None:
        logger.error("No action with action_id 'docs|qa|approve_reply' found.")
        return
    

    # Split action.value on "|" and get team, channel and message_ts
    team, channel, message_ts = action.get("value").split("|") # team|channel|message_ts
        
    print(f"ack - action_id:'docs|qa|approve_reply', values - team: {team}, channel: {channel}, message_ts: {message_ts}")
    # Acknowledge the interaction
    ack()

    # Log the body of the interaction payload
    pp.pprint(body)

    user_id = body["user"]["id"]
    bot_id = body["message"]["bot_id"]
    
    blocks_without_sendbutton = copy.deepcopy(body["message"]["blocks"])
    del blocks_without_sendbutton[-1]["accessory"]
    print('blocks_without_sendbutton:')
    pp.pprint(blocks_without_sendbutton)
    
    try:
        app.client.reactions_add(
            channel=body["channel"]["id"],
            timestamp=body["message"]["ts"],
            name="white_check_mark",
            as_user=True
        )
    except SlackApiError as e:
        logger.error(f"Error adding reaction: {e}")


    # Send a reply to the thread confirming that the message action was successful
    try:
        app.client.chat_postMessage(
            channel=body["channel"]["id"],
            thread_ts=body["message"]["ts"],
            user_id=user_id,            
            text=f"<@{user_id}> gave the thumbs-up, forwarding message...",
        )
        app.client.chat_postMessage(
            team=team,
            channel=channel,
            thread_ts=message_ts,
            text=body["message"]["text"],
            blocks=blocks_without_sendbutton,
            user_id=bot_id
        )

    except SlackApiError as e:
        logger.error(f"Error sending confirmation: {e}")


# The open_modal shortcut opens a plain old modal
# Shortcuts require the command scope
@app.shortcut("open_modal")
def open_modal(ack, shortcut, client, logger):
    # Acknowledge shortcut request
    ack()

    try:
        # Call the views.open method using the WebClient passed to listeners
        result = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "My App"},
                "close": {"type": "plain_text", "text": "Close"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/block-elements|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>.",
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>",
                            }
                        ],
                    },
                ],
            },
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3001)))
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN" + slack_bot_suffix]).start()
