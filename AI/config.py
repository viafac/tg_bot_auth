import os
import logging
import psycopg2

from dotenv import load_dotenv
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from AI.templates import recommendation_prompt

load_dotenv()
logging.basicConfig(level=logging.INFO)

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="gpt-4")
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

vectorstore = PGVector(
    connection_string=os.getenv("DATABASE_URL"),
    collection_name="books",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt)


def format_recommendations(books):
    return "\n\n".join([
        f"📚 {title}\nАвтор: {author}\nОписание: {description}\n— Мы рекомендуем эту книгу!"
        for title, description, author in books
    ])

