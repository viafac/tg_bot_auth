import pytest

from sqlalchemy.exc import SQLAlchemyError
from bot.queries.employers import EmployersObj


@pytest.mark.asyncio
async def test_create_employer(db_session, mocker):
    test_employer = await EmployersObj().create(db_session, full_name='Asd Asd', email='asd@ventionteams.com')

    assert test_employer is not None
    assert test_employer.full_name == 'Asd Asd'

    mocker.patch.object(db_session, 'add', side_effect=SQLAlchemyError("DB error"))
    test_employer_2 = await EmployersObj().create(db_session, full_name='AA bb', email='ab@ventionteams.com')
    assert test_employer_2 is None
