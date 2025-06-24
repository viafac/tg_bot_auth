from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    role = State()
    email = State()
    confirm_code = State()
