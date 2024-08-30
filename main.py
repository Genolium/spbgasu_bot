import os
import asyncio, logging, threading, utility
from aiogram import types
from aiogram.types import BotCommand
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

BOT_URL = ""

async def set_user_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="🤖 Перезапустить бота")
    ]
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeDefault()) 

async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True)  
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    os.environ['BOT_URL'] = f"https://t.me/{bot_username}"
    await dp.start_polling(bot, on_startup=on_startup)   
    await set_user_commands(bot)

def run_web():
    app.run(debug=False, host='0.0.0.0', port=5000)

async def main():
    create_db()

    #запускаем бота
    t = threading.Thread(target=run_web)
    t.start()

    #запускаем веб-часть
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())