from aiogram import types

admin_buttons = [
    [types.KeyboardButton(text="Создать опрос")],
    [types.KeyboardButton(text="Создать рассылку")],
    [types.KeyboardButton(text="Список администраторов")]
]

admin_keyboard = types.ReplyKeyboardMarkup(keyboard=admin_buttons, resize_keyboard=True)