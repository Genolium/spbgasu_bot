#           УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from filters.is_admin import IsAdminIDFilter
from keyboardrs.admin_keyboards import admin_keyboard
from utility.util import *
from utility.db import *
from utility.states import *

universal_router=Router()

# ОТВЕТ НА ВОПРОС ИЗ ГРУППЫ АДМИНОВ
@universal_router.message(F.chat.id)
async def answer_to_user(message: types.Message, state: FSMContext):
    if message.reply_to_message:
        if str(message.chat.id) == str(ADMIN_GROUP_ID) and  message.reply_to_message.forward_origin.sender_user.id is not None:
            await bot.send_message(chat_id=message.reply_to_message.forward_origin.sender_user.id, text="*Вам пришел ответ от администрации\! *\n", parse_mode=ParseMode.MARKDOWN_V2)
            await message.copy_to(chat_id=message.reply_to_message.forward_origin.sender_user.id)
            await state.clear()
            
# ОТВЕТ НА ОПРОСНИК
@universal_router.callback_query(F.data.startswith("quiz_"))
async def send_response(call: types.CallbackQuery):
    data = call.data.split("_")
    add_quiz_response(call.from_user.id,data[1],data[2])
    await call.message.edit_reply_markup()
    await call.message.answer("Спасибо за ваш ответ!")