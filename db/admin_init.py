import asyncio
import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import select
from database import async_session_factory
from models import AppUsers, Roles, Permissions, Employers, TelegramUsers, RolePermissions

load_dotenv()


async def init_role(session_factory):
    async with session_factory() as session:
        try:
            role = Roles(id=uuid.uuid4(), name='Admin', description='Head admin')
            session.add(role)
            await session.commit()
            return role.id
        except Exception as e:
            await session.rollback()
            raise e


async def init_permission(session_factory):
    async with session_factory() as session:
        try:
            permission = Permissions(id=uuid.uuid4(), name='All CRUD', description='CRUD for all objects')
            session.add(permission)
            await session.commit()
            return permission.id
        except Exception as e:
            await session.rollback()
            raise e


async def init_employer(session_factory) -> uuid.UUID:
    full_name = os.getenv('ADMIN_FULL_NAME')
    email = os.getenv('ADMIN_EMAIL')

    async with session_factory() as session:
        employer = Employers(
            id=uuid.uuid4(),
            full_name=full_name,
            email=email,
            is_verified=True,
        )
        session.add(employer)
        await session.commit()
        return employer.id


async def init_telegram_user(session_factory) -> uuid.UUID:
    tg_str = os.getenv("ADMIN_TG_ID")

    async with session_factory() as session:
        new_tg_user = TelegramUsers(
            id=uuid.uuid4(),
            telegram_id=tg_str,
            username=os.getenv("ADMIN_FULL_NAME"),
        )
        session.add(new_tg_user)
        await session.commit()
        return new_tg_user.id


async def admin_init(session_factory):
    telegram_user_id = await init_telegram_user(session_factory)
    employer_id = await init_employer(session_factory)
    role_id = await init_role(session_factory)
    permission_id = await init_permission(session_factory)

    async with session_factory() as session:
        admin = AppUsers(
            id=uuid.uuid4(),
            telegram_user_id=telegram_user_id,
            employer_id=employer_id,
            role_id=role_id,
            is_active=True,
        )
        session.add(admin)

        new_role_permission = RolePermissions(
            role_id=role_id,
            permission_id=permission_id,
        )
        session.add(new_role_permission)
        await session.commit()
        return True


if __name__ == '__main__':
    asyncio.run(admin_init(async_session_factory))
