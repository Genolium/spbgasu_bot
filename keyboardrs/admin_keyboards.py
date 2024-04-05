from aiogram import types

#кнопки администратора
admin_buttons = [
    [types.KeyboardButton(text="🗳️Создать опрос")],
    [types.KeyboardButton(text="📨Создать рассылку")],
    [types.KeyboardButton(text="📋Список администраторов")],
    [types.KeyboardButton(text="🫥Режим пользователя")],
    [types.KeyboardButton(text="⚙️Расширенные настройки")]
]

admin_keyboard = types.ReplyKeyboardMarkup(keyboard=admin_buttons, resize_keyboard=True)


#кнопки администратора в режиме простого пользователя
fake_user_buttons = [
    [types.KeyboardButton(text="Вернуться⏪")],
    [types.KeyboardButton(text="FAQ📋")],
    [types.KeyboardButton(text="Календарь мероприятий🗓️")],
    [types.KeyboardButton(text="Написать обращение в студсовет✍")],
    [types.KeyboardButton(text="Наши контакты📞")]
]

fake_user_keyboard = types.ReplyKeyboardMarkup(keyboard=fake_user_buttons, resize_keyboard=True)