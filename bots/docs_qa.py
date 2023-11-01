import timeit
import pprint

from slack_sdk.errors import SlackApiError
import openai.error
import utils.slack_utils as slack_utils
from bots.structured_log import bot_log, BotLogEntry
from docs_qa.rag_with_typesense import rag_with_typesense
from channel_msg_categorize.run_chain import (
    run_chain_async as run_channel_msg_categorize,
)


pp = pprint.PrettyPrinter(indent=2)
chain_name = "[docs]"


async def run_bot_async(app, hitl_config, say, msg_body, text):
    src_evt_context = slack_utils.get_event_context(msg_body)

    print(f"src_msg_metadata: ")
    pp.pprint(src_evt_context)

    main_channel_id = msg_body.get("event").get("channel")
    target_channel_id = main_channel_id
    qa_channel_id = hitl_config.get("qa_channel", "")
    src_msg_link = ""

    hitl_enabled = qa_channel_id != "" and hitl_config.get("enabled")

    # override target_channel_id if hitl enabled
    if hitl_enabled:
        target_channel_id = qa_channel_id
        src_msg_link = slack_utils.get_message_permalink(app, msg_body)

    print(
        f"hitl enabled: {hitl_enabled}, main_channel_id: {main_channel_id}, qa_channel_id: {qa_channel_id}"
    )

    # categorize message, respond to messages of type '[Support Request]'
    msg_categorize_start_time = timeit.default_timer()
    response = await run_channel_msg_categorize(text)
    message_category = response["text"]
    print(f"Message category: {message_category}")


    bot_log(BotLogEntry(
        slack_context= src_evt_context,
        elapsed_ms= slack_utils.time_s_to_ms(timeit.default_timer() - msg_categorize_start_time),
        step_name= 'categorize_message',
        payload= {"user_input": text, "bot_name": 'docs', 'message_category': message_category}
    ))

    if message_category != "[Support Request]":
        # we only handle support requests, so done
        print(
            f'Assistant does not know what to do with messages of category: "{message_category}"'
        )
        return

    quoted_input = text.replace("\n", "\n>")

    thread1_text = (
        f'Incoming message from <#{main_channel_id}>\n>  "{quoted_input}"'
        if hitl_enabled
        else f'Let me figure out which team would be best suited to handle the following inquiry:\n>  "{quoted_input}"'
    )

    blocks = (
        [{}]
        if not hitl_enabled
        else [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{src_msg_link}|Incoming message> from <#{main_channel_id}>",
                },
            },
        ]
    )

    startMsg = app.client.chat_postMessage(
        text=thread1_text,
        blocks=blocks,
        channel=target_channel_id,
    )

    thread_ts = startMsg["ts"]
    print(f"startMsg.ts: {thread_ts}")
    pp.pprint(startMsg)

    if hitl_enabled:
        thread1 = app.client.chat_postMessage(
            text=f"Running {chain_name} chain...",
            channel=qa_channel_id,
            thread_ts=thread_ts,
        )
    else:
        thread1 = say(
            text="This should only take a few seconds...", thread_ts=thread_ts
        )

    try:
        start = timeit.default_timer()
        response = await rag_with_typesense(text)
        end = timeit.default_timer()
                
        bot_log(BotLogEntry(
            slack_context= src_evt_context,
            elapsed_ms= slack_utils.time_s_to_ms(end - start),
            step_name= 'rag_with_typesense',
            payload= {"user_input": text, "bot_name": 'docs',
                      'search_terms': response['search_terms'],
                      'answer': response['result'],
                      'source_urls': response['source_urls'],
                      } 
        ))
    except openai.error.ServiceUnavailableError as e:
        print(f"OpenAI API error: {e}")
        app.client.chat_postMessage(
            thread_ts=thread_ts,
            text=f"OpenAI API error: {e}",
            channel=target_channel_id,
        )

    answer = response["result"]

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Search terms extracted:\n> {response['search_terms']}",
            },
        },
        {"type": "section", "text": {"type": "mrkdwn", "text": "Results"}},
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": answer},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": f"Send"},
                "value": f'{src_evt_context.team}|{src_evt_context.channel}|{src_evt_context.ts}',
                "action_id": "docs|qa|approve_reply",
            },
        },
    ]
    reply_text = (
        f"Suggested reply:\n{answer}"
        if hitl_enabled
        else f'Here is what I found related to your query:\n   >"{text}"\n\n_{answer}_'
    )

    try:
        app.client.chat_update(
            channel=thread1["channel"],
            ts=thread1["ts"],
            text=reply_text,
            blocks=blocks,
            as_user=True,
        )
    except SlackApiError as e:
        print(f"Error attempting to delete temp bot message {e}")

    # print(f'{answer}')
    # say(thread_ts=thread_ts,
    #     text=f'>{answer}')

    # known_path_segment = "altinn/docs/content"
    known_path_segment = "https://docs.altinn.studio"



    # Process source documents
    source_docs = response["source_documents"]
    for i, doc in enumerate(source_docs):
        print(f"doc {i}:\n{doc}")
        source = doc["metadata"]["source"]
        path_segment_index = source.index(known_path_segment)
        if path_segment_index >= 0:
            slice_start = (
                (-1 * len(source)) + path_segment_index + len(known_path_segment) + 1
            )
            # print(f'slice_start: {slice_start}')
            source = "https://docs.altinn.studio/" + source[slice_start:]
            source = source.rpartition("/")[0]

        page_content = doc["page_content"].replace("\n", "\n>")

        sourceSummary = f"Source #{i+1}: {source}"
        source_blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{sourceSummary}"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"Send",
                    },
                    "value": f'{src_evt_context.team}|{src_evt_context.channel}|{src_evt_context.ts}',
                    "action_id": "docs|qa|approve_reply",
                },
            },
        ]
        app.client.chat_postMessage(
            thread_ts=thread_ts,
            text=sourceSummary,
            blocks=source_blocks,
            channel=target_channel_id,
        )

    say(
        thread_ts=thread_ts,
        channel=target_channel_id,
        text=f"Time to retrieve response: {round(end - start, 1)} seconds.",
    )
