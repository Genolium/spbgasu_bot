from aiogram import types

advanced_buttons = [
    [types.KeyboardButton(text="⏪")],
    [types.KeyboardButton(text="📅🖋️Добавить мероприятие в календарь")],
    [types.KeyboardButton(text="🖋️🎥Изменить фото в мероприятии")],
    [types.KeyboardButton(text="📋Список администраторов")],
    [types.KeyboardButton(text="📌❓Добавить вопрос в FAQ📝")],
    [types.KeyboardButton(text="🖋️Изменить свои учетные данные")],
    [types.KeyboardButton(text="📝Добавить администратора")],
    [types.KeyboardButton(text="🗑️Удалить администратора по id")],    
]

advanced_keyboard = types.ReplyKeyboardMarkup(keyboard=advanced_buttons, resize_keyboard=True)