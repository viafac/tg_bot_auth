from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

registration_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yes, let's start", callback_data="reg_yes"),
         InlineKeyboardButton(text="No, maybe later", callback_data="reg_no")]
    ]
)

reg_roles_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Employer", callback_data="employer"),
            InlineKeyboardButton(text="Guest", callback_data="guest"),
        ],
        [
            InlineKeyboardButton(text="Exit", callback_data="exit")
        ]
    ]
)


back_to_email = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Try again", callback_data="back_to_email")],
    ]
)


resend_code = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Resend", callback_data="resend_code")],
        [InlineKeyboardButton(text="Exit", callback_data="exit")],
    ]
)
