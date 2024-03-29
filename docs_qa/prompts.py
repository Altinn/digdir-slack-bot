'''
===========================================
        Module: Prompts collection
===========================================
'''
# Note: Precise formatting of spacing and indentation of the prompt template is important for Llama-2-7B-Chat,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

stage1_analyze_query = """You are a skilled customer service agent with many years experience evaluating incoming support requests related to Altinn, a data collection system for government agencies.

1. If the question is not in English, first translate to English. 

2. Categorize the [USER PROMPT] based on the following categories:

[Support Request]
Request for help, usually includes a question.

[For Your Information]
Not a support request, usually a general information sharing message.

[Pull request announcement]
Information about a Github pull request, also called a PR

[None of the above]
Catch all category if none of the above categories matches well.

3. Finally, return the category, original language code and name.
"""

qa_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: 
{context}

Question: {question}

First, answer the question in English, including relevant source code examples when possible.
"""

def qa_template(target_language_name):
    translate_hint = '\nOnly return the helpful answer below, along with relevant source code examples when possible.\n'

#     if target_language_name != None and target_language_name != "English":
#         translate_hint = f"""
#         First, answer the question in English, including relevant source code examples when possible.

#         Finally, translate your helpful answer to "{target_language_name}", using UTF-8 encoding.\n\n""" 

    prompt_text = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

""" + translate_hint + "\nHelpful answer:\n"
    
    # print(f'Prompt text:\n{prompt_text}')
    return prompt_text


generate_search_phrases_template = """Please analyze the contents of the following documentation article and generate a list of English phrases that you would expect to match the following document. 
DO NOT include the phrases "Altinn Studio", "Altinn 3" or "Altinn apps".

Document:
{document}
"""