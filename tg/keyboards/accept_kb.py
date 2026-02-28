from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def accept_decline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да ✅", callback_data="accept"), InlineKeyboardButton(text="Нет ⛔", callback_data="decline")]
        ]
    )
