from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from services import get_stats
from db import User


stats_router = Router()


@stats_router.message(F.text == "Статистика 📊")
async def profile(message: Message, state: FSMContext):
    await state.clear()
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
    )

    stats = get_stats()
    text = (
        "<b>Статистика 📊</b>\n\n"
        f"<b>👤 Количество пользователей:</b> {stats["count_users"]}\n"
        f"<b>📝 Количество докладов:</b> {stats["count_docs"]}\n\n"
        f"🏆 <b>ТОП-3 пользователя по докладам:</b>\n"
    )
    for i, top in enumerate(stats["top_3"], start=1):
        text += f"{i}. <i>{top.name}</i> - {top.cnt}\n"

    await message.answer(text, parse_mode=ParseMode.HTML)