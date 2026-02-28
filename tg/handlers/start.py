from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext

from db import User
from tg.keyboards import main_kb


start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    user, created = User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
    )

    if not created:
        await message.answer(
            f"Рад снова видеть! 👋\n\n"
            "<i>Выбирай что тебе нужно на клавиатуре снизу и поехали! 🚀</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=main_kb()
        )
    else:
        await message.answer(
            f"Приветствую! 👋\n\n"
            "Я - бот, который может сделать за тебя доклад!\n\n"
            "👉 Всё что тебе нужно, это расписать твою задачу и я сделаю всё как ты попросишь!\n\n"
            "<i>Выбирай что тебе нужно на клавиатуре снизу и поехали! 🚀</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=main_kb()
        )