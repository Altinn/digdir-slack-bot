import json
import pprint

from slack_sdk.errors import SlackApiError
import openai
import utils.slack_utils as slack_utils
from bots.structured_log import bot_log, BotLogEntry
from github_qa.rag_issues import rag_with_typesense
from channel_msg_categorize.run_chain import (
    run_chain_async as run_channel_msg_categorize,
)


pp = pprint.PrettyPrinter(indent=2)
chain_name = "[gh-issues]"


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
    categorize_response = await run_channel_msg_categorize(text)
    message_category = categorize_response["text"]
    print(f"Message category: {message_category}")

    bot_log(
        BotLogEntry(
            slack_context=src_evt_context,
            elapsed_ms=slack_utils.time_s_to_ms(categorize_response["duration"]),
            step_name="categorize_message",
            payload={
                "user_input": text,
                "bot_name": "gh_issues",
                "message_category": message_category,
            },
        )
    )

    # if message_category != "[Support Request]":
    #     # we only handle support requests, so done
    #     print(
    #         f'Assistant does not know what to do with messages of category: "{message_category}"'
    #     )
    #     return

    first_message_text = (
        f"<{src_msg_link}|Incoming message> from <#{main_channel_id}>"
        if hitl_enabled
        else f""
    )
    quoted_input = text.replace("\n", "\n>")

    if hitl_enabled:
        startMsg = app.client.chat_postMessage(
            text=first_message_text,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": first_message_text,
                    },
                }
            ],
            channel=target_channel_id,
        )
        thread_ts = startMsg["ts"]
    else:
        thread_ts = src_evt_context.ts

    if hitl_enabled:
        thread1 = app.client.chat_postMessage(
            text=f"Running {chain_name} chain...",
            channel=qa_channel_id,
            thread_ts=thread_ts,
        )
    else:
        thread1 = say(text="Checking Github issues", thread_ts=thread_ts)

    try:
        rag_response = await rag_with_typesense(text)

        payload = {
            "user_input": text,
            "bot_name": chain_name,
            "search_queries": rag_response["search_queries"],
            "answer": rag_response["result"],
            "source_urls": rag_response["source_urls"],
            "relevant_urls": rag_response["relevant_urls"],
        }
        if rag_response["rag_success"] is not None:
            payload["rag_success"] = rag_response["rag_success"]

        bot_log(
            BotLogEntry(
                slack_context=src_evt_context,
                elapsed_ms=slack_utils.time_s_to_ms(rag_response["durations"]["total"]),
                durations=rag_response["durations"],
                step_name="rag_with_typesense",
                payload=payload,
            )
        )

    except openai.APIConnectionError as e:
        rag_with_typesense_error = f"Azure OpenAI error: {e}"
    except openai.RateLimitError as e:
        rag_with_typesense_error = f"Azure OpenAI service is busy right now, let's try again"
    except openai.APIStatusError as e:
        rag_with_typesense_error = f"Azure OpenAI API error: {e}"
    except Exception as ex:
        rag_with_typesense_error = f"Error: {ex}"

    if rag_with_typesense_error:
        print(rag_with_typesense_error)
        return


    answer = rag_response["result"]
    relevant_sources = rag_response["relevant_urls"]

    answer_block = (
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": answer},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": f"Send"},
                "value": f"{src_evt_context.team}|{src_evt_context.channel}|{src_evt_context.ts}",
                "action_id": "docs|qa|approve_reply",
            },
        }
        if hitl_enabled
        else {
            "type": "section",
            "text": {"type": "mrkdwn", "text": answer},
        }
    )

    blocks = [answer_block]

    if len(relevant_sources) > 0:
        links_mrkdwn = "\n".join(
            f"<{source['url']}|{source['title']}>" for source in relevant_sources
        )
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Relevant links:\n{links_mrkdwn}"},
            }
        )

    blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Generated in {round(rag_response['durations']['total'], ndigits=1)} seconds."},
        })

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

    # Process source documents
    source_blocks = []
    source_docs = rag_response["source_documents"]
    for i, doc in enumerate(source_docs):
        # print(f"doc {i}:\n{doc}")
        source = doc["metadata"]["source"]
        vector_distance = round(doc.get("vector_distance"), 3)
        
        source_summary = f"{i+1}: <{source}|{doc.get('title','')}> [{doc.get('state', '')}]"

        label_list = doc.get('labels', [])
        if len(label_list) > 0:
            label_list = [f"`{label}`" for label in label_list]
            source_summary += f"\n> labels: {' '.join(label_list)}"                
        
        source_blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": source_summary},
            })

    source_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Processing times (sec):\n```\n{json.dumps(rag_response['durations'], indent=2)}```",
                },
            })

    # TODO: add to channel config 
    if True:
        app.client.chat_postMessage(
            thread_ts=thread_ts,
            text="Retrieved Github issues",
            blocks=source_blocks,
            channel=target_channel_id,
        )
