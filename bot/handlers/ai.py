import logging

from aiogram import types, Router
from AI.config import format_recommendations, conn, retriever

ai_router = Router()


@ai_router.message()
async def handle_message(message: types.Message):
    user_query = message.text

    try:
        docs = retriever.get_relevant_documents(user_query)
        if not docs:
            await message.answer("Sorry, no matching books found.")
            return

        doc_ids = [doc.metadata.get("id") for doc in docs if doc.metadata.get("id")]

        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, description, author
                FROM books
                WHERE id = ANY(%s)
            """, (doc_ids,))
            books = cur.fetchall()

        if not books:
            await message.answer("Sorry, no books found in the database.")
            return

        formatted_books = format_recommendations(books)
        await message.answer(formatted_books)

    except Exception as e:
        logging.error(e)
        await message.answer("⚠️ An error occurred. Please try again.")


