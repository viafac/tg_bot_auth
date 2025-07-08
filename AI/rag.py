import logging

from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from AI.config import conn, llm
from AI.templates import recommendation_prompt
from AI.validation import PromptInput
from db.default_data_init import embeddings_model

load_dotenv()

logging.basicConfig(level=logging.INFO)

user_context = {}


def semantic_search(query, top_k=3):
    query_vector = embeddings_model.embed_query(query)
    vector = [float(v) for v in query_vector]

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, description, author 
                FROM books 
                ORDER BY embedding <-> %s::vector 
                LIMIT %s
            """, (vector, top_k))
            return cur.fetchall()


def rag_answer(user_query: str) -> tuple[str, list[tuple]]:
    results = semantic_search(user_query)

    books_text = "\n\n".join([
        f"{title}\n{author}\n{description}" for title, description, author in results
    ])

    try:
        validated = PromptInput(books=books_text, question=user_query)
    except ValueError as e:
        raise ValueError(f"Validation error: {e}")

    chain = LLMChain(llm=llm, prompt=recommendation_prompt)
    response = chain.run(books=validated.books, question=validated.question)

    return response, results
