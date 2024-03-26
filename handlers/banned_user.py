#           ОБРАБОТКА АДМИНСКИХ КОМАНД
from aiogram import types,Router
from filters.is_banned import IsBannedFilter


banned_private_router=Router()
banned_private_router.message.filter(IsBannedFilter())

@banned_private_router.message()
async def you_are_banned(message: types.Message):
    await message.answer("Вы были заблокированы администрацией бота",reply_markup=types.ReplyKeyboardRemove())