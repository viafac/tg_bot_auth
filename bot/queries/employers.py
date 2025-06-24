import logging
import uuid


from bot.queries.interface import CRUD
from db.database import async_session_factory
from db.models import Employers

logger = logging.getLogger(__name__)


class EmployersObj(CRUD):
    async def create(self, session: async_session_factory, full_name: str, email: str):
        try:
            new_employer = Employers(
                id=uuid.uuid4(),
                full_name=full_name,
                email=email,
                is_verified=True
            )
            session.add(new_employer)
            await session.commit()
            return new_employer
        except Exception as e:
            await session.rollback()
            logger.error(e)
            return None

    async def update(self):
        pass

    async def remove(self):
        pass

    async def get_obj(self):
        pass

    async def read(self):
        pass
