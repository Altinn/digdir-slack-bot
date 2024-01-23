'''
===========================================
        Module: Prompts collection
===========================================
'''
# Note: Precise formatting of spacing and indentation of the prompt template is important for Llama-2-7B-Chat,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

stage1_analyze_query = """You are a skilled customer service agent with many years experience evaluating incoming support requests related to Altinn, a data collection system for government agencies.

You will be asked to categorize the [USER PROMPT] based on the following categories:

[Support Request]
Request for help, usually includes a question.

[For Your Information]
Not a support request, usually a general information sharing message.

[Pull request announcement]
Information about a Github pull request, also called a PR

[None of the above]
Catch all category if none of the above categories matches well.

Analyze the following text and return the specified structured data points.
"""