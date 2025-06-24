from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    email = State()
    confirm_code = State()
