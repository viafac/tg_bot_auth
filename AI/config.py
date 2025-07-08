import psycopg2
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="gpt-4")

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
