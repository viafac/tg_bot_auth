import os
import pytest_asyncio

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.models import Base, TelegramUsers, Employers, AppUsers, Roles

load_dotenv()

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('TEST_POSTGRES_USER')}:{os.getenv('TEST_POSTGRES_PASSWORD')}"
    f"@{os.getenv('TEST_POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('TEST_POSTGRES_DB')}"
    )


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def clear_all_tables(db_engine):
    async with db_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))


@pytest_asyncio.fixture
async def db_session(db_engine, clear_all_tables):
    session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def sample_tg_users(db_session):
    users = [
        TelegramUsers(telegram_id='111', username='A'),
        TelegramUsers(telegram_id='222', username='B'),
        TelegramUsers(telegram_id='333', username='C'),
    ]
    db_session.add_all(users)
    await db_session.commit()
    return users


@pytest_asyncio.fixture
async def sample_employers(db_session):
    employers = [
        Employers(full_name='AA',email='aa@ventionteams.com'),
        Employers(full_name='BB', email='aa@gmail.com')
    ]
    db_session.add_all(employers)
    await db_session.commit()
    return employers


@pytest_asyncio.fixture
async def sample_roles(db_session):
    roles = [
        Roles(name='Admin', description='Head admin'),
        Roles(name='User', description='Employer'),
        Roles(name='Guest', description='Guest'),
    ]
    db_session.add_all(roles)
    await db_session.commit()
    return roles


@pytest_asyncio.fixture
async def sample_app_users(db_session, sample_tg_users, sample_employers, sample_roles):
    app_users = [
        AppUsers(
            telegram_user_id=sample_tg_users[0].id,
            employer_id=sample_employers[0].id,
            role_id=sample_roles[1].id
        ),
        AppUsers(
            telegram_user_id=sample_tg_users[1].id,
            employer_id=sample_employers[1].id,
            role_id=sample_roles[2].id
        ),
    ]
    db_session.add_all(app_users)
    await db_session.commit()
    return app_users
