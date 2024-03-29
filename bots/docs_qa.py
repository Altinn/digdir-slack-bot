import json
import pprint
import timeit
from typing import Callable
from bots.config import lookup_config 

from slack_sdk.errors import SlackApiError
import openai
import utils.slack_utils as slack_utils
from bots.structured_log import bot_log, BotLogEntry
from utils.markdown import split_to_sections

from docs_qa.stage1_analyze import query as stage1_analyze
from docs_qa.rag_manual_stuff import rag_with_typesense


pp = pprint.PrettyPrinter(indent=2)
chain_name = "[docs]"


async def run_bot_async(app, hitl_config, say, msg_body, text, first_thread_ts):

    src_evt_context = slack_utils.get_event_context(msg_body)

    enableDebugMessages = lookup_config(src_evt_context, 'enableDebugMessages', True)
    print(f'enableDebugMessages: {enableDebugMessages}')


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

    # categorize message, respond to messages of type 'Support Request'
    start = timeit.default_timer()
    stage1_result = await stage1_analyze(text)
    stage1_duration = round(timeit.default_timer() - start, 1)

    bot_log(
        BotLogEntry(
            slack_context=src_evt_context,
            elapsed_ms=slack_utils.time_s_to_ms(stage1_duration),
            step_name="stage1_analyze",
            payload={
                "bot_name": "docs",
                "english_user_query": stage1_result.questionTranslatedToEnglish,
                "original_user_query": text,
                "user_query_language_code": stage1_result.userInputLanguageCode,
                "user_query_language_name": stage1_result.userInputLanguageName,
                "content_category": stage1_result.contentCategory,
            },
        )
    )

    if not "Support Request" in stage1_result.contentCategory:
        # we only handle support requests, so done
        print(
            f'Assistant does not know what to do with messages of category: "{stage1_result.contentCategory}"'
        )
        return

    first_message_text = (
        f"<{src_msg_link}|Incoming message> from <#{main_channel_id}>"
        if hitl_enabled
        else f""
    )
    
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

    busy_reading_msg = "Reading Altinn Studio docs..."
    will_translate_msg = ''

    if stage1_result.userInputLanguageCode == 'no':
        will_translate_msg = "Oversetter til norsk snart..."
    else:
       will_translate_msg = f"We will also translate this message to {stage1_result.userInputLanguageName}."
    

    if hitl_enabled:
        first_thread_ts = app.client.chat_postMessage(
            text=f"Running {chain_name} chain...",
            channel=qa_channel_id,
            thread_ts=thread_ts,
        )
    else:
        if first_thread_ts != None:
            try:
                app.client.chat_update(
                    channel=first_thread_ts["channel"],
                    ts=first_thread_ts["ts"],
                    text=busy_reading_msg,
                    as_user=True,
                )
            except SlackApiError as e:
                print(f"Error attempting to delete temp bot message {e}")
        else:
            first_thread_ts = say(text=busy_reading_msg, thread_ts=thread_ts)

    translated_msg_callback = None

    if will_translate(stage1_result):
        second_thread_ts = say(text=will_translate_msg, thread_ts=thread_ts)            
        translated_msg_callback = update_slack_msg_callback(app, second_thread_ts)

    rag_with_typesense_error = None

    try:
        rag_start = timeit.default_timer()
        
        rag_response = await rag_with_typesense(stage1_result.questionTranslatedToEnglish, 
                                                stage1_result.userInputLanguageName, 
                                                False, 
                                                update_slack_msg_callback(app, first_thread_ts),
                                                translated_msg_callback)

        payload = {
            "bot_name": "docs",
            "original_user_query": rag_response.get('original_user_query', ''),
            "english_user_query": rag_response.get("english_user_query", ""),
            "user_query_language_code": rag_response.get("user_query_language_code", ''),
            "user_query_language_name": rag_response.get("user_query_language_name", ''),
            "english_answer": rag_response.get("english_answer", ""),
            "translated_answer": rag_response.get("translated_answer", ""),
            "search_queries": rag_response["search_queries"],
            "source_urls": rag_response["source_urls"],
            "relevant_urls": rag_response["relevant_urls"],
            "not_loaded_urls": rag_response.get("not_loaded_urls", []),
        }
        if rag_response["rag_success"] is not None:
            payload["rag_success"] = rag_response["rag_success"]

    except openai.APIConnectionError as e:
        rag_with_typesense_error = f"Azure OpenAI error: {e}"
    except openai.RateLimitError as e:
        rag_with_typesense_error = f"Azure OpenAI service is busy right now, let's try again"
    except openai.APIStatusError as e:
        rag_with_typesense_error = f"Azure OpenAI API error: {e}"
    except Exception as ex:
        rag_with_typesense_error = f"Error: {ex}"


    if rag_with_typesense_error:
        # try to log the error, before letting the user know that something went wrong

        print(f'\n\nERROR running rag_with_typesense: {rag_with_typesense_error}\n\n')

        payload = {
            "bot_name": "docs",
            "original_user_query": text,
            "error": rag_with_typesense_error,
            "rag_success": False
        }

        bot_log(
            BotLogEntry(
                slack_context=slack_utils.get_context_from_thread_response(src_evt_context.ts, first_thread_ts),
                elapsed_ms=slack_utils.time_s_to_ms(timeit.default_timer() - rag_start),
                durations={},
                step_name="rag_with_typesense",
                payload=payload,
            )
        )

        app.client.chat_postMessage(
            thread_ts=thread_ts,
            text=rag_with_typesense_error,
            channel=target_channel_id,
        )

        return

    # call finalize_answer
    finalize_answer(app, first_thread_ts, rag_response.get('english_answer', ''), rag_response, 
                    rag_response["durations"]["total"] + stage1_duration - rag_response["durations"]["translation"])

    if will_translate(stage1_result):
        finalize_answer(app, second_thread_ts, rag_response.get('translated_answer', ''), rag_response, 
                        rag_response["durations"]["translation"])
        

    bot_log(
        BotLogEntry(
            slack_context=slack_utils.get_context_from_thread_response(src_evt_context.ts, first_thread_ts),
            elapsed_ms=slack_utils.time_s_to_ms(rag_response["durations"]["total"]),
            durations=rag_response["durations"],
            step_name="rag_with_typesense",
            payload=payload,
        )
    )
    
    # known_path_segment = "altinn/docs/content"
    known_path_segment = "https://docs.altinn.studio"

    source_docs = rag_response["source_documents"]
    not_loaded_urls = rag_response["not_loaded_urls"]
    debug_blocks = []
    fields_list = "*Retrieved articles*\n"
    not_loaded_list = ""

    # Data rows
    for i, doc in enumerate(source_docs):
        source = doc["metadata"]["source"]
        path_segment_index = source.index(known_path_segment)
        if path_segment_index >= 0:
            slice_start = (
                (-1 * len(source)) + path_segment_index + len(known_path_segment) + 1
            )
            source = "https://docs.altinn.studio/" + source[slice_start:]
            source = source.rpartition("/")[0] + "/"

        source_text = source.replace("https://docs.altinn.studio/", "")

        fields_list += f"#{i+1}: <{source}|{source_text}>\n"

    for i, url in enumerate(not_loaded_urls):
        not_loaded_list += (
            f"#{i+1}: <{url}|{url.replace('https://docs.altinn.studio/', '')}>\n"
        )

    search_queries_summary = "\n> ".join(rag_response["search_queries"])
    debug_blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Phrases generated for retrieval:\n> {search_queries_summary}",
            },
        }
    )

    debug_blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": fields_list,
            },
        }
    )
    if len(not_loaded_list) > 0:
        debug_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Retrieved, but not used:*\n{not_loaded_list}",
                },
            }
        )

    duration_report = rag_response['durations']
    duration_report['analyze'] = stage1_duration
    duration_report['total'] += stage1_duration

    debug_blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Processing times (sec):\n```\n{json.dumps(duration_report, indent=2)}```",
            },
        }
    )

    if enableDebugMessages:
        app.client.chat_postMessage(
            thread_ts=thread_ts,
            text="Debug message",
            blocks=debug_blocks,
            channel=target_channel_id,
        )

def will_translate(stage1_result):
    return stage1_result.userInputLanguageCode != 'en'


def update_slack_msg_callback(slack_app, thread_ts) -> Callable:

    content_chunks: list[str] = []

    def inner(partial_response):

        content_chunks.append(partial_response)

        sections = split_to_sections("".join(content_chunks))

        blocks = []
        for i, paragraph in enumerate(sections):
            blocks.insert(i, {
                "type": "section",
                "text": {"type": "mrkdwn", "text": paragraph},
            })

        print(f'Partial response update for channel \'{thread_ts["channel"]}\' ts {thread_ts["ts"]}, time: {round(timeit.default_timer(), 1)}')

        try:
            slack_app.client.chat_update(
                channel=thread_ts["channel"],
                ts=thread_ts["ts"],
                text='...',
                blocks=blocks,
                as_user=True,
            )
        except SlackApiError as e:
            print(f"Error attempting to update Slack message {e}")
    
    return inner

def finalize_answer(app, thread_ts, answer, rag_response, duration):
        
    relevant_sources = rag_response["relevant_urls"]

    sections = split_to_sections(answer)

    blocks = []
    for i, paragraph in enumerate(sections):
        blocks.insert(i, {
            "type": "section",
            "text": {"type": "mrkdwn", "text": paragraph},
        })


    if len(relevant_sources) > 0:
        links_mrkdwn = "\n".join(
            f"<{source['url']}|{source['title']}>" for source in relevant_sources
        )
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"For more information:\n{links_mrkdwn}",
                },
            }
        )

    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Generated in {round(duration, ndigits=1)} seconds.\n" +
                f"Please give us your feedback with a :+1: or :-1:",
            },
        }
    )

    try:
        app.client.chat_update(
            channel=thread_ts["channel"],
            ts=thread_ts["ts"],
            text='Final answer',
            blocks=blocks,
            as_user=True,
        )
    except SlackApiError as e:
        print(f"Error attempting to update temp bot message {e}")

    