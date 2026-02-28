from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext

import asyncio

from db import User
from tg.keyboards import profile_kb


profile_router = Router()


@profile_router.message(F.text == "Мой профиль 👤")
async def profile(message: Message, state: FSMContext):
    await state.clear()
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
    )

    docs_count = user.documents.count()
    await message.answer(
        f"👤 <b>Имя</>: {user.name}{f" (@{user.username})" if user.username else ""}\n"
        f"🛫 <b>Зарегистрировались</b>: {user.created_at.strftime("%d.%m.%Y %H:%M")}\n\n"
        f"📈 <b>Количество сгенерированных докладов</b>: {docs_count}",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb() if docs_count else None
    )


@profile_router.callback_query(F.data == "list_docs")
async def docs(callback: CallbackQuery):
    user, _ = User.get_or_create(
        user_id=callback.from_user.id,
        defaults={
            "name": callback.from_user.first_name,
            "username": callback.from_user.username
        }
    )
    await callback.answer()

    for doc in user.documents:
        file = FSInputFile(doc.filepath)

        await callback.message.answer_document(
            document=file,
            caption=f"<b>{doc.filename}</b>\n\n<i>Сделан в: {doc.created_at.strftime("%d.%m.%Y %H:%M")}</i>",
            parse_mode=ParseMode.HTML
        )
        await asyncio.sleep(0.05)