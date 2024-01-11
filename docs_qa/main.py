import json
import pprint

import openai

from docs_qa.rag_manual_stuff import rag_with_typesense
from channel_msg_categorize.run_chain import (
    run_chain_async as run_channel_msg_categorize,
)


pp = pprint.PrettyPrinter(indent=2)

async def main(text):

    # categorize message, respond to messages of type '[Support Request]'
    categorize_response = await run_channel_msg_categorize(text)
    message_category = categorize_response["text"]

    if message_category != "[Support Request]":
        # we only handle support requests, so done
        print(
            f'Assistant does not know what to do with messages of category: "{message_category}"'
        )
        return

    print("Reading Altinn Studio docs...")

    rag_with_typesense_error = None

    try:
        rag_response = await rag_with_typesense(text)    
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


    # print results
    print(f"""rag_with_typesense response:
          
\"english_answer\": 
{rag_response.get('english_answer', '')}

User query language code: \'{rag_response.get('user_query_language_code')}\', name: \'{rag_response.get('user_query_language_name')}\'
\"translated_answer\": 
{rag_response.get('translated_answer', '')}

""")
    
    relevant_sources = rag_response["relevant_urls"]

    if len(relevant_sources) > 0:
        links_summary = "\n".join(
            f"{source['title']} - {source['url']}" for source in relevant_sources
        )
        print(links_summary)

    print(f"Generated in {round(rag_response['durations']['total'], ndigits=1)} seconds.")

    # known_path_segment = "altinn/docs/content"
    known_path_segment = "https://docs.altinn.studio"

    source_docs = rag_response["source_documents"]
    not_loaded_urls = rag_response["not_loaded_urls"]
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

    print(f"Phrases generated for retrieval:\n> {search_queries_summary}")
    print(f'{fields_list}')

    if len(not_loaded_list) > 0:
        print(f"*Retrieved, but not used:*\n{not_loaded_list}")

    print(json.dumps(rag_response['durations'], indent=2))

    