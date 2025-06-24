import logging
import uuid

from sqlalchemy import select
from bot.queries.interface import CRUD
from db.database import async_session_factory
from db.models import AppUsers, TelegramUsers, Roles

logger = logging.getLogger(__name__)


class AppUserObj(CRUD):
    async def create(self, session: async_session_factory, telegram_id: uuid, employer_id: uuid) -> bool:
        try:
            role_result = await session.execute(select(Roles).where(Roles.name == 'User'))
            role_id = role_result.scalar_one_or_none().id
            if not role_id:
                logger.error("Role 'User' not found")
                return False

            new_user = AppUsers(
                telegram_user_id=telegram_id,
                employer_id=employer_id,
                role_id=role_id,
                is_active=True,
            )
            session.add(new_user)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            logger.error(f"Error when creating a user: {e}")
            return False

    async def read(self, session: async_session_factory):
        pass

    async def update(self):
        pass

    async def remove(self):
        pass

    async def get_obj(self, session: async_session_factory, telegram_id: int):
        pass

    @staticmethod
    async def is_user_registered(session: async_session_factory, telegram_id: str):
        tg_user = await session.execute(select(TelegramUsers).where(TelegramUsers.telegram_id == telegram_id))
        selected_tg_user = tg_user.scalars().first()
        return True if selected_tg_user else False

    @staticmethod
    async def is_working_email(email: str) -> bool:
        email = email.lower().split("@")
        if email[-1] == "ventionteams.com":
            return True
        return False
