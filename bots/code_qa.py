import timeit

from code_qa.main import code_query


async def run_bot_async(app, hitl_config, say, msg_body, text):
        # first, send a normal reply and then a thread
    startMsg =  say(f'Sounds like you are interested in help with advanced validation rules, let me check for something similar.')
    thread_ts = startMsg['ts']
    # print(f'startMsg: {startMsg}')
    thread1 = say(text='This should only take a few moments...',
            thread_ts=thread_ts)
    # print(f'thread1: {thread1}')
    start = timeit.default_timer()
    response = await code_query(text)
    end = timeit.default_timer()

    answer = response["result"]

    try:
        app.client.chat_update(channel=thread1['channel'], ts=thread1['ts'],
                            text=f'Here are the most relevant validation rule implementations I found related to your query:\n>  \"{text}\"',
                            as_user=True)                
    except SlackApiError as e:
        print(f'Error attempting to delete temp bot message {e}')

    # print(f'{answer}')
    # say(thread_ts=thread_ts,
    #     text=f'{answer}')

    known_path_segment = 'altinn/docs/content'
    # Process source documents
    source_docs = response['source_documents']
    for i, doc in enumerate(source_docs):
        # print(f'doc {i}:\n{doc}')
        source = doc.metadata["source"]
        print(f'source: {source}')
        codepath = source.replace(".summary.txt", "")
        code_contents = ''
        with open(codepath, 'r') as codefile:
            code_contents = codefile.read()

        # path_segment_index = source.index(known_path_segment)
        # if (path_segment_index >= 0):
        #     slice_start = (-1 * len(source)) + path_segment_index + len(known_path_segment) + 1
        #     # print(f'slice_start: {slice_start}')
        #     source = "https://docs.altinn.studio/" + source[slice_start:]     
        #     source = source.rpartition('/')[0]       
        sourceSummary = f'Source #{i+1}: \n{codepath}\n\n{doc.page_content}\n\n```\n{code_contents}\n```'
        say(thread_ts=thread_ts,
            text=sourceSummary)
        
    say(thread_ts=thread_ts,
        text=f"Time to retrieve response: {round(end - start, 1)} seconds.")