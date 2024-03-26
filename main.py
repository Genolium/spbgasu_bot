import asyncio, logging, sys
from aiogram import types
from utility.util import *
from web.index import app
from utility.db import create_db
from handlers.user_private import user_router
from handlers.admin_private import admin_private_router
from handlers.universal_private import universal_router
from handlers.banned_user import banned_private_router

#включаем логгирование
logging.basicConfig(level=logging.INFO)

dp.include_router(banned_private_router)
dp.include_router(admin_private_router)
dp.include_router(user_router)
dp.include_router(universal_router)

async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

async def run_web():
    await app.run(debug=True)

async def main():
    create_db()

    if len(sys.argv) > 1 and sys.argv[1] == "web":
        await run_web()
    else:
        await run_bot()

if __name__ == "__main__":
    asyncio.run(main())