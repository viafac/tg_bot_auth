import logging
import uuid

from bot.queries.interface import CRUD
from db.database import async_session_factory
from db.models import TelegramUsers


logger = logging.getLogger(__name__)


class TelegramUser(CRUD):
    async def create(self, session: async_session_factory, telegram_id: str, username: str):
        try:
            new_tg_user = TelegramUsers(
                id=uuid.uuid4(),
                telegram_id=telegram_id,
                username=username,
            )
            session.add(new_tg_user)
            await session.commit()
            return new_tg_user
        except Exception as e:
            await session.rollback()
            logger.error(f"Error when creating a user: {e}")
            return None

    async def update(self):
        pass

    async def remove(self):
        pass

    async def get_obj(self):
        pass

    async def read(self):
        pass
