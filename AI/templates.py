from langchain_core.prompts import PromptTemplate

recommendation_prompt = PromptTemplate.from_template("""
You are a helpful library assistant. Use only the books from the database to answer the question. 
Do not invent or reference any books that are not listed.

Books:
{books}

User question:
{question}
""")

