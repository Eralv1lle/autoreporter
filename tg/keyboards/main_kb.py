from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мой профиль 👤"), KeyboardButton(text="Сгенерировать доклад 📝")],
            [KeyboardButton(text="Статистика 📊")]
        ],
        resize_keyboard=True
    )