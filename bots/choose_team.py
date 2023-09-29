import timeit

from slack_bolt import App
from slack_sdk.errors import SlackApiError
from utils.llm_utils import extract_json_from_response
import utils.slack_utils

from team_qa_choose.main import team_query
from channel_msg_categorize.run_chain import (
    run_chain_async as run_channel_msg_categorize,
)

json_doc_keyword = "JSON Document:".lower()
chain_name = "[choose_team]"


async def run_bot_async(app, hitl_config, say, msg_body, text):
    assert isinstance(app, App), "app must be an instance of slack_bolt.App"

    src_msg_metadata = utils.slack_utils.get_message_metadata(msg_body)

    main_channel_id = msg_body.get("event").get("channel")
    target_channel_id = main_channel_id
    qa_channel_id = hitl_config.get("qa_channel", '')

    hitl_enabled = qa_channel_id != '' and hitl_config.get("enabled")

    # override target_channel_id if hitl enabled
    if hitl_enabled:
        target_channel_id = qa_channel_id
    
    print(
        f"hitl enabled: {hitl_enabled}, main_channel_id: {main_channel_id}, qa_channel_id: {qa_channel_id}"
    )

    # categorize message, respond to messages of type '[Support Request]'
    response = await run_channel_msg_categorize(text)
    message_category = response["text"]
    print(f"Message category: {message_category}")

    if message_category != "[Support Request]":
        # we only handle support requests, so done
        print(
            f'Assistant does not know what to do with messages of category: "{message_category}"'
        )
        return

    print(f"Starting {chain_name} chain...")

    quoted_input = text.replace("\n", "\n>")

    thread1_text = (
        f'Incoming message from <#{main_channel_id}>\n>  "{quoted_input}"'
        if hitl_enabled
        else f'Let me figure out which team would be best suited to handle the following inquiry:\n>  "{quoted_input}"'
    )

    startMsg = app.client.chat_postMessage(
        text=thread1_text,
        channel=target_channel_id,
        metadata=src_msg_metadata,
    )

    thread_ts = startMsg["ts"]

    if hitl_enabled:
        thread1 = app.client.chat_postMessage(
            text=f"Running {chain_name} chain...", channel=qa_channel_id, thread_ts=thread_ts
        )
    else:
        thread1 = say(
            text="This should only take a few seconds...", thread_ts=thread_ts
        )
    # print(f'thread1: {thread1}')
    start = timeit.default_timer()
    response = await team_query(text)
    end = timeit.default_timer()

    answer = response["text"]
    print(f"Complete response: {answer}")

    [json_dict, answer] = extract_json_from_response(answer, json_doc_keyword)
    blocks = []

    if json_dict:
        print(f"json_doc:\n{json_dict}")

        # Extract the desired values
        team_name = json_dict.get("team-name")
        confidence = json_dict.get("confidence-1-to-10")
        reply = f"Answer:\n{answer}\nTeam: *{team_name}*"

        blocks = [
            {"type": "section", "text": {"type": "plain_text", "text": "Results"}},
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": answer},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Team: *{team_name}*\nConfidence score (1 to 10): {confidence}\n",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Confirm"},
                    "value": f"{team_name}",
                    "action_id": "[team][choose][confirm]",
                },
            },
        ]
    else:
        reply = (
            f"Unfortunately, I was not able to determine which team would be relevant."
        )
        print(f"json_doc_keyword '{json_doc_keyword}' not found in llm response")

    print(reply)

    try:
        app.client.chat_update(
            channel=thread1["channel"],
            ts=thread1["ts"],
            blocks=blocks,
            text=reply,
            as_user=True,
        )
    except SlackApiError as e:
        print(f"Error attempting to delete temp bot message {e}")
