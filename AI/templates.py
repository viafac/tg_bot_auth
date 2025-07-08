from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from AI.config import llm

recommendation_prompt = PromptTemplate.from_template("""
You are a helpful library assistant. Use ONLY the books listed below to answer the user's question. 
Do NOT make up any books. Your answer must be concise and follow this structure for each recommendation:

Title: <Book Title>  
Author: <Book Author>  
Description: <Brief Description>  
Note: We recommend this book.

Books:
{books}

User question:
{question}

Respond in the specified format. Answer only in English.
""")

recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt)

