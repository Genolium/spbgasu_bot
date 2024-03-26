from aiogram import types

main_buttons=[
    [types.KeyboardButton(text="FAQ📋")],
    [types.KeyboardButton(text="Календарь мероприятий🗓️")],
    [types.KeyboardButton(text="Написать обращение в студсовет✍")],
    [types.KeyboardButton(text="Наши контакты📞")],
]
main_keyboard = types.ReplyKeyboardMarkup(keyboard=main_buttons,resize_keyboard=True)