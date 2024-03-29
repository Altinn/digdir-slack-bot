"""
===========================================
        Module: Slack bot Bolt app
===========================================
"""
import asyncio
import pprint
import copy

from slack_bolt import App
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

import utils.slack_utils as slack_utils
from utils.general import env_var
# from bots.choose_team import run_bot_async as bot_choose_team
from bots.code_qa import run_bot_async as bot_code_qa
from bots.docs_qa import run_bot_async as bot_docs_qa
# from bots.github_qa import run_bot_async as bot_github_qa
from bots.structured_log import bot_log, update_reactions, BotLogEntry



# Install the Slack app and get xoxb- token in advance
app = App(
    token=env_var("SLACK_BOT_TOKEN"),
    signing_secret=env_var("SLACK_BOT_SIGNING_SECRET"),
)

bot_query_word_code = "[code] "
bot_query_word_docs = "[docs] "
bot_query_word_team = "[team] "
bot_query_word_gh_issues = "[gh-issues] "

pp = pprint.PrettyPrinter(indent=2)

hitl_config = {"enabled": False, "qa_channel": env_var("REVIEW_CHANNEL_ID")}


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
    # pp.pprint(body)
    src_evt_context = slack_utils.get_event_context(body)

    evt = body["event"]
    if evt.get("type") == "message":
        if evt.get("subtype") == "message_deleted":
            logger.info(f"Ignoring message_deleted event.")

        clean_text = text = evt.get("text", "")
        print(f"user input: {text}")
        if not evt.get("thread_ts"):
            # message is not in a thread

            bot_name = None
            if text.startswith(bot_query_word_docs):
                bot_name = "docs"
                clean_text = text.replace(bot_query_word_docs, "")
            elif text.startswith(bot_query_word_code):
                bot_name = "code"
                clean_text = text.replace(bot_query_word_code, "")
            elif text.startswith(bot_query_word_team):
                bot_name = "team"
                clean_text = text.replace(bot_query_word_team, "")
            elif text.startswith(bot_query_word_gh_issues):
                bot_name = "gh-issues"
                clean_text = text.replace(bot_query_word_gh_issues, "")            
            elif not text.startswith("["):
                bot_name = "docs"
                
            first_thread_ts = say(text="Thinking...", thread_ts=evt.get('ts'))


            entry = BotLogEntry(
                slack_context= src_evt_context,
                elapsed_ms= 0,
                step_name= 'select_bot',
                payload= {"user_input": clean_text, "bot_name": bot_name}
            )
            bot_log(entry)

            if bot_name == "docs":
                asyncio.run(bot_docs_qa(app, hitl_config, say, body, clean_text, first_thread_ts))
            elif bot_name == "code":
                asyncio.run(bot_code_qa(app, hitl_config, say, body, clean_text))
            # elif bot_name == "team":
            #     asyncio.run(bot_choose_team(app, hitl_config, say, body, clean_text))
            # elif bot_name == "gh-issues":
            #     asyncio.run(bot_github_qa(app, hitl_config, say, body, clean_text))
            elif not text.startswith("["):
                asyncio.run(bot_docs_qa(app, hitl_config, say, body, clean_text))
            else:
                print(f"Unknown query type: '{text}'")

            
@app.action("approve_button")
def update_message(ack):
    ack()
    print(f"approve button pressed")

def handle_reaction_events(event):

    # TODO: check if in channel before getting current message reactions

    try:
        message_info = app.client.reactions_get(
            channel=event["item"]["channel"],
            timestamp=event["item"]["ts"]
        )
        reactions = message_info["message"].get("reactions", [])
        # print(f"Current reactions: {reactions}")

        if reactions != None:
            item_context = slack_utils.get_reaction_item_context(event)
            update_reactions(item_context, reactions)

    except SlackApiError as e:
        print(f"Error fetching reactions: {e}")


@app.event("reaction_added")
def handle_reaction_added(event, say):
    handle_reaction_events(event)    


@app.event("reaction_removed")
def handle_reaction_removed(event, say):
    handle_reaction_events(event)

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
    action = next(
        (
            action
            for action in body.get("actions", [])
            if action.get("action_id") == "docs|qa|approve_reply"
        ),
        None,
    )

    if action is None:
        logger.error("No action with action_id 'docs|qa|approve_reply' found.")
        return

    # Split action.value on "|" and get team, channel and message_ts
    team, channel, message_ts = action.get("value").split(
        "|"
    )  # team|channel|message_ts

    print(
        f"ack - action_id:'docs|qa|approve_reply', values - team: {team}, channel: {channel}, message_ts: {message_ts}"
    )
    # Acknowledge the interaction
    ack()

    # Log the body of the interaction payload
    pp.pprint(body)

    user_id = body["user"]["id"]
    bot_id = body["message"]["bot_id"]

    blocks_without_sendbutton = copy.deepcopy(body["message"]["blocks"])

    if "accessory" in blocks_without_sendbutton[-2]:
        del blocks_without_sendbutton[-2]["accessory"]

    print("blocks_without_sendbutton:")
    pp.pprint(blocks_without_sendbutton)

    try:
        app.client.reactions_add(
            channel=body["channel"]["id"],
            timestamp=body["message"]["ts"],
            name="white_check_mark",
            as_user=True,
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
            user_id=bot_id,
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


def main():
    app.start(port=int(env_var("PORT", 3000)))
    SocketModeHandler(app, env_var("SLACK_APP_TOKEN")).start()

if __name__ == "__main__":
    main()