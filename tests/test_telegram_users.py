import pytest

from sqlalchemy.exc import SQLAlchemyError
from bot.queries.telegram_users import TelegramUser


@pytest.mark.asyncio
async def test_create_tg_user(db_session, mocker):
    test_tg_user = await TelegramUser().create(db_session, telegram_id='1111', username='Asd')

    assert test_tg_user is not None
    assert test_tg_user.telegram_id == '1111'
    assert test_tg_user.username == 'Asd'

    mocker.patch.object(db_session, 'add', side_effect=SQLAlchemyError("DB error"))
    test_tg_user_2 = await TelegramUser().create(db_session, telegram_id='222', username='Qwe')
    assert test_tg_user_2 is None
