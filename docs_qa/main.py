import json
import pprint
import openai
import timeit

from .config import env_var
from docs_qa.stage1_analyze import query as stage1_analyze
from docs_qa.rag_manual_stuff import rag_with_typesense


pp = pprint.PrettyPrinter(indent=2)

async def main(text):

    print(f'USE_AZURE_OPENAI_API: {env_var("USE_AZURE_OPENAI_API")}')

    # categorize message, respond to messages of type '[Support Request]'
    start = timeit.default_timer()
    stage1_result = await stage1_analyze(text)
    duration = round(timeit.default_timer() - start, 1)

#   english_user_query: {stage1_result.questionTranslatedToEnglish}
    print(f"""stage1_result in {duration} seconds:
  language_code: {stage1_result.userInputLanguageCode}
  language_name: {stage1_result.userInputLanguageName}
  original_user_query: {text}
  content_category: {stage1_result.contentCategory}
""")

    # TODO: remove this return
    #return

    message_category = stage1_result.contentCategory

    if not "Support Request" in message_category:
        # we only handle support requests, so done
        print(
            f'Assistant does not know what to do with messages of category: "{message_category}"'
        )
        return

    busy_reading_msg = "Reading Altinn Studio docs..."

    if stage1_result.userInputLanguageCode == 'no':
        busy_reading_msg = "Leser relevante artikler fra Altinn Studio dokumentasjonen..."
    elif stage1_result.userInputLanguageCode == 'nn':
        busy_reading_msg = "Relevante artiklar frå Altinn Studio dokumentasjonen lesast..."
    
    print(busy_reading_msg)

    rag_error = None

    try:
        rag_response = await rag_with_typesense(text, stage1_result.userInputLanguageName)    
    except openai.APIConnectionError as e:
        rag_error = f"Azure OpenAI error: {e}"
    except openai.RateLimitError as e:
        rag_error = f"Azure OpenAI service is busy right now, let's try again"
    except openai.APIStatusError as e:
        rag_error = f"Azure OpenAI API error: {e}"
    except Exception as ex:
        rag_error = f"Error: {ex}"


    if rag_error:
        print(rag_error)
        return


    # print results
    print(f"""rag_with_typesense response:
          
\"english_answer\": 
{rag_response.get('english_answer', '')}

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

    # enableDebugMessages = bot_config(SlackContext()).get("enableDebugMessages", True)
    # print(f"enabeDebugMessages : {enableDebugMessages }" )