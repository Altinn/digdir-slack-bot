'''
===========================================
        Module: Prompts collection
===========================================
'''

qa_template = """First, if the question is not in English, first translate to English.
Then, use the following Github issue data to answer the user's question, always using English.
If you don't know the answer, just say that you don't have sufficient information, don't try to make up an answer.

Context: {context}

Question: {question}

Return a helpful answer below, being sure to mention which provided Github issues were relevant, and whether the issue is open or closed.
Helpful answer:
"""
