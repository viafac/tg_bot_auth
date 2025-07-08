import logging

from aiogram import types, Router
from AI.rag import rag_answer, user_context

ai_router = Router()


@ai_router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_query = message.text

    try:
        response, results = rag_answer(user_query)
        await message.answer(response)

        user_context[user_id] = {
            "last_results": results,
            "last_query": user_query
        }

    except ValueError as ve:
        logging.warning(f"Validation failed: {ve}")
        await message.answer("⚠️ Please clarify your request.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await message.answer("⚠️ An error occurred, please try again.")
