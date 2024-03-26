from aiogram import types

quiz_buttons = [
    [types.KeyboardButton(text="Добавить ответ")],
    [types.KeyboardButton(text="Закончить создание опроса")]
]

quiz_keyboard = types.ReplyKeyboardMarkup(keyboard=quiz_buttons, resize_keyboard=True)