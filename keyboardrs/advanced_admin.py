from aiogram import types

advanced_buttons = [
    [types.KeyboardButton(text="📝Добавить администратора")],
    [types.KeyboardButton(text="🗑️Удалить администратора по id")],
    [types.KeyboardButton(text="📌❓Добавить вопрос в FAQ📝")],
    [types.KeyboardButton(text="📅🖋️Добавить мероприятие в календарь")],
    [types.KeyboardButton(text="⏪")]
]

advanced_keyboard = types.ReplyKeyboardMarkup(keyboard=advanced_buttons, resize_keyboard=True)