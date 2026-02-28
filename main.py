import asyncio
import os
import logging

from tg import start_bot
from db import init_db
from config import config


async def main():
    os.makedirs(f"{config.DOCS_DIRECTORY}/", exist_ok=True)
    init_db()
    await start_bot()


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
    except Exception as err:
        print(f"Упал: {err}")