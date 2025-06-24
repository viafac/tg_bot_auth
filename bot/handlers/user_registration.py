from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.keyboards.user_kbs import reg_roles_kb, registration_kb, back_to_email, resend_code
from bot.notifications.send_reg_code import send_verification_code, generate_code
from bot.queries.employers import EmployersObj
from bot.queries.telegram_users import TelegramUser
from bot.queries.app_users import AppUserObj
from bot.states.user_states import Registration
from db.database import async_session_factory

user_reg_router = Router()


@user_reg_router.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = str(message.chat.id)

    async with async_session_factory() as session:
        if await AppUserObj().is_user_registered(session=session, telegram_id=telegram_id):
            await message.answer("You have already registered!")
        else:
            await message.answer(
                "Welcome! 👋 Let's get you registered so I can better assist you. "
                "It will only take a minute. Shall we get started?",
                reply_markup=registration_kb
            )
            return


@user_reg_router.callback_query(F.data == "reg_no")
async def reg_stop(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.answer("If you change your mind, just type /start. See you soon!")


@user_reg_router.callback_query(F.data == "reg_yes")
async def reg_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    text = (
        "<b>Please choose how to register:</b>\n\n"
        "🏢 <b>I'm a company employee</b>\n"
        "▫️ Requires registration\n"
        "▫️ Can browse and rent <b>multiple books</b>\n"
        "▫️ Full control of own orders (view, update, cancel)\n"
        "▫️ Can edit personal profile\n"
        "▫️ Can create and manage own wishlist\n\n"
        "👤 <b>Continue as Guest</b>\n"
        "▫️ No account required\n"
        "▫️ Can browse locations and books\n"
        "▫️ Can rent <b>only one book at a time</b>\n"
        "▫️ No access to personal profile or wishlist"
    )
    await callback.message.edit_text(text, reply_markup=reg_roles_kb, parse_mode='HTML')


@user_reg_router.callback_query(F.data == "exit")
async def reg_exit(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete_reply_markup()
    await callback.message.edit_text("See you soon!")


@user_reg_router.callback_query(F.data == "guest")
async def reg_role_guest(callback: CallbackQuery):
    telegram_id = str(callback.message.chat.id)
    username = callback.from_user.username
    async with async_session_factory() as session:
        reg_new_user = await TelegramUser().create(session=session, telegram_id=telegram_id, username=username)
    if reg_new_user:
        await callback.message.delete_reply_markup()
        await callback.message.edit_text(
            f"✅ <b>Registration Complete!</b>\n"
            f"👤 You are now registered as <b>{username}</b>\n\n"
            f"🚀 Enjoy using the bot! Here are some useful commands to get started:\n\n"
            f"📚 /books – Explore our full book collection\n"
            f"📍 /locations – Discover available pickup locations\n"
            f"📋 /orders – View and manage your orders\n"
            f"✉️ /contact – Contact admin or leave feedback\n",
            parse_mode='HTML'
        )
        await callback.answer()
    else:
        await callback.message.answer('Please try again later.')


@user_reg_router.callback_query(F.data == "employer")
async def reg_role_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.edit_text("Please enter your working (company) email:")
    await state.set_state(Registration.email)


@user_reg_router.message(Registration.email)
async def reg_name(message: Message, state: FSMContext):
    working_email = await AppUserObj().is_working_email(email=message.text)
    if working_email:
        await state.update_data(email=message.text)
        code = generate_code()
        send = send_verification_code(to_email=message.text, code=code)
        if send:
            await message.answer('Please enter verification code: ')
            await state.update_data(verification_code=code)
            await state.set_state(Registration.confirm_code)
        else:
            await message.answer('Please try again later')
    else:
        await message.answer('Incorrect email, please try again.', reply_markup=back_to_email)
        await state.set_state(Registration.email)


@user_reg_router.message(Registration.confirm_code)
async def reg_confirm(message: Message, state: FSMContext):
    state_data = await state.get_data()
    code = state_data['verification_code']
    email = state_data['email']
    if code == message.text:
        async with async_session_factory() as session:
            new_tg_user = await TelegramUser().create(
                session=session,
                telegram_id=str(message.from_user.id),
                username=message.from_user.username
            )
            new_employer = await EmployersObj().create(
                session=session,
                email=email,
                full_name=message.from_user.full_name
            )
            await AppUserObj().create(session=session, telegram_id=new_tg_user.id, employer_id=new_employer.id)
            await message.answer(
                f"✅ <b>Registration Complete!</b>\n"
                f"👤 You are now registered as <b>{message.from_user.full_name}</b>\n\n"
                f"🚀 Enjoy using the bot! Here are some useful commands to get started:\n\n"
                f"📚 /books – Explore our full book collection\n"
                f"📍 /locations – Discover available pickup locations\n"
                f"📋 /orders – View and manage your orders\n"
                f"⭐ /wishlists – View and manage your wishlists\n"
                f"📋 /feedback – contact admin or give a feedback\n",
                parse_mode='HTML'
            )
            await state.clear()
    else:
        await message.answer('Verification code is wrong, please try again', reply_markup=resend_code)


@user_reg_router.callback_query(F.data == "back_to_email")
async def reg_back_to_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer('Please enter your working email: ')
    await state.set_state(Registration.email)


@user_reg_router.callback_query(F.data == "resend_code")
async def reg_resend_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    state_data = await state.get_data()
    code = generate_code()
    send = send_verification_code(to_email=state_data['email'], code=code)
    if send:
        await callback.message.answer('Please enter verification code: ')
        await state.update_data(verification_code=code)
        await state.set_state(Registration.confirm_code)
    else:
        await callback.message.answer('Error')
