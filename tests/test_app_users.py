import pytest

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from bot.queries.app_users import AppUserObj
from db.models import TelegramUsers


@pytest.mark.asyncio
async def test_create_app_user(db_session, sample_tg_users, sample_employers, sample_roles, mocker):
    telegram_user = sample_tg_users[0]
    employer = sample_employers[0]
    result_1 = await AppUserObj().create(db_session, telegram_id=telegram_user.id, employer_id=employer.id)

    assert result_1 is True

    mocker.patch.object(db_session, 'execute', side_effect=SQLAlchemyError("DB error"))
    result_2 = await AppUserObj().create(db_session, telegram_id=telegram_user.id, employer_id=employer.id)

    assert result_2 is False


@pytest.mark.asyncio
async def test_is_user_registered(db_session, sample_tg_users):
    result = await db_session.execute(select(TelegramUsers))
    tg_users = result.scalars().first()

    registered = await AppUserObj().is_user_registered(session=db_session, telegram_id=tg_users.telegram_id)
    not_registered = await AppUserObj().is_user_registered(session=db_session, telegram_id='555')

    assert registered is True
    assert not_registered is False


@pytest.mark.asyncio
async def test_is_working_email(db_session):
    valid_email = await AppUserObj().is_working_email(email='asd@ventionteams.com')
    invalid_email = await AppUserObj().is_working_email(email='asd@mail.ru')

    assert valid_email is True
    assert invalid_email is False

