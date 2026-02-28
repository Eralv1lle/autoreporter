from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ParseMode

import docx
import PyPDF2

from services import make_docx
from tg.states import UserStates
from tg.keyboards import accept_decline_kb
from db import User, Document
from config import config
from services.ai import check_prompt


report_router = Router()


@report_router.message(F.text == "Сгенерировать доклад 📝")
async def report_request(message: Message, state: FSMContext):
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
    )

    await message.answer(
        "Отлично! 😊\n\n"
        "Для создания доклада, пожалуйста, напишите тему доклада ✍️\n\n"
        "Для более хорошего и развёрнутого доклада, можете указать:\n"
        "- Ваши инициалы, класс\n"
        "- Распишите какие вы хотите видеть стили в презентации (шрифт и размер шрифта)\n"
        "- Распишите структуру и объём доклада\n\n"
        "Жду сообщения от вас и сразу приступаю к докладу! 🚀"
    )
    await state.set_state(UserStates.waiting_for_report)


@report_router.message(UserStates.waiting_for_report)
async def report_get(message: Message, state: FSMContext, bot: Bot):
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "name": message.from_user.first_name,
            "username": message.from_user.username
        }
    )

    if message.document:
        filename = message.document.file_name.lower()

        if filename.endswith(".txt") or filename.endswith(".docx") or filename.endswith(".pdf"):
            file = await bot.get_file(message.document.file_id)
            content = await bot.download_file(file.file_path)

            if filename.endswith(".txt"):
                request = content.read().decode("utf-8")

            elif filename.endswith(".docx"):
                doc = docx.Document(content)
                request = "\n".join([p.text for p in doc.paragraphs])

            else:
                r = PyPDF2.PdfReader(content)
                request = "".join([page.extract_text() for page in r.pages])

            mes = await message.answer("Извлекаю задачу... 📤")
            check = await check_prompt(request[:400])
            if not check:
                await mes.edit_text("К сожалению, мы не можешь исполнить этот запрос. Попробуйте ещё раз")
                return

            await mes.edit_text(
                f"Отлично! Извлёк содержимое файла <b>{filename}</b>\n\n"
                "Ваш запрос (первые 222 символа):\n\n"
                f"<blockquote>{request[:222]}</blockquote>\n\n"
                "Начинать доклад?",
                parse_mode=ParseMode.HTML,
                reply_markup=accept_decline_kb()
            )
            await state.update_data(request=request)

        else:
            await message.answer("Данный тип файлов не поддерживается. Попробуйте: .txt, .docx, .pdf")
    else:
        if not message.text:
            await message.answer('Пожалуйста, введите запрос текстом')
            return

        request = message.text

        mes = await message.answer("Анализирую задачу... 🤔")
        check = await check_prompt(request[:400])
        if not check:
            await mes.edit_text("К сожалению, мы не можешь исполнить этот запрос. Попробуйте ещё раз")
            return

        await mes.edit_text(
            "Отлично!\n\n"
            "Ваш запрос:\n\n"
            f"<blockquote>{request}</blockquote>\n\n"
            "Начинать доклад?",
            parse_mode=ParseMode.HTML,
            reply_markup=accept_decline_kb()
        )
        await state.update_data(request=request)


@report_router.callback_query(F.data == "accept")
async def accept(callback: CallbackQuery, state: FSMContext):
    user, _ = User.get_or_create(
        user_id=callback.from_user.id,
        defaults={
            "name": callback.from_user.first_name,
            "username": callback.from_user.username
        }
    )

    data = await state.get_data()
    request = data.get("request")

    await callback.message.answer(
        f"Отлично!\n\n"
        f"Ваш запрос (первые 222 символа):\n\n"
        f"<blockquote>{request[:222]}</blockquote>\n\n"
        f"Начинаю выполнять доклад... 🪶",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

    cnt = user.documents.count()
    filename = await make_docx(request, callback.from_user.id, cnt + 1)
    file = FSInputFile(f"docs/{filename}")

    await callback.message.answer_document(
        document=file,
        caption=f"Ваш доклад готов!\n\n<i>{filename}</i>",
        parse_mode=ParseMode.HTML
    )
    await state.clear()
    Document.create(user=user, filename=filename, filepath=f"{config.DOCS_DIRECTORY}/{filename}")


@report_router.callback_query(F.data == "decline")
async def decline(callback: CallbackQuery):
    user, _ = User.get_or_create(
        user_id=callback.from_user.id,
        defaults={
            "name": callback.from_user.first_name,
            "username": callback.from_user.username
        }
    )

    await callback.message.answer("Хорошо! Заново введите запрос или прикрепите файл (.txt, .docx, .pdf)")
    await callback.answer()
