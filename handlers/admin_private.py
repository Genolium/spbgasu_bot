#           ОБРАБОТКА АДМИНСКИХ КОМАНД
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode
from aiogram.utils.deep_linking import decode_payload

from filters.is_admin import IsAdminIDFilter
from keyboardrs.admin_keyboards import admin_keyboard
from keyboardrs.quiz_create_keyboard import quiz_keyboard
from utility.util import *
from utility.db import *
from utility.states import *

admin_private_router=Router()
admin_private_router.message.filter(IsAdminIDFilter())

# ПРИВЕТСТВИЕ
@admin_private_router.message(CommandStart())
async def start_cmd(message: types.Message, command: CommandObject):
    args = command.args
    if args and int(args):
        a = int(args)
        button_url = f'tg://user?id={a}'
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Ссылка", url=button_url)]])
        await bot.send_message(message.chat.id, text=f'Ссылка на id {a}:\n\n<a href="tg://user?id={a}">ссылка</a>', reply_markup=markup, parse_mode=ParseMode.HTML)
    elif not get_user(message.from_user.id):
       add_user(message.from_user.id)
    await message.answer('Привет, администратор ' + message.from_user.username,reply_markup=admin_keyboard)

# ВЫВОД СПИСКА АДМИНОВ
@admin_private_router.message(F.text == "Список администраторов")
async def admin_list(message: types.Message):
    l = ""
    for admin in get_all_admins():
        print(admin)
        id = str(admin[0])
        user = admin[1]
        l += f"{user}: id={id}\n"
    await message.answer(l)

# ДОБАВЛЕНИЕ АДМИНА 
@admin_private_router.message(F.text == "Добавить администратора")
async def add_admin_message(message: types.Message, state: FSMContext):
    await message.answer("Введите имя нового администратора")
    await state.set_state(Add_Admin_States.waiting_for_username)

@admin_private_router.message(Add_Admin_States.waiting_for_username)
async def add_admin_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Введите id админа (его можно узнать с помощью команды /id в боте)")
    await state.set_state(Add_Admin_States.waiting_for_id)

@admin_private_router.message(Add_Admin_States.waiting_for_id)
async def add_admin_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    new_admin_data = await state.get_data()
    add_admin(new_admin_data["id"], new_admin_data["username"])    
    await message.reply("Новый администратор успешно добавлен")
    await state.clear()

# УДАЛЕНИЕ АДМИНА ПО ID
@admin_private_router.message(F.text == "Удалить администратора по id")
async def delete_admin_message(message: types.Message, state: FSMContext):
    await message.answer("Введите Telegram ID администратора, которого нужно удалить")
    await state.set_state(Delete_Admin_States.waiting_for_id)

@admin_private_router.message(Delete_Admin_States.waiting_for_id)
async def delete_admin_id(message: types.Message, state: FSMContext):
    tg_id = message.text
    delete_admin(tg_id)
    await message.reply("Администратор успешно удален")
    await state.clear()    

# РАССЫЛКИ
@admin_private_router.message(F.text == "Создать рассылку")
async def send_newsletter(message: types.Message, state: FSMContext):
    await message.answer('''Напишите текст рассылки, который будет отправлен всем пользователям бота\n
Вы можете использовать оформление из Telegram (жирный текст, курсив, спойлер и т.д.)''')
    await state.set_state(NewsletterStates.waiting_for_content)

@admin_private_router.message(NewsletterStates.waiting_for_content)
async def get_newsletter_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message)
    user_data = await state.get_data()
    
    keyboard = types.InlineKeyboardMarkup(row_width=2,inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Отправить рассылку", callback_data="send_newsletter"),
            types.InlineKeyboardButton(text="Отмена", callback_data="cancel_newsletter")
        ]
    ])
    await message.answer(f"Вы уверены в том, что хотите разослать данное сообщение?", reply_markup=keyboard)
    await state.set_state(NewsletterStates.confirm_newsletter)

@admin_private_router.callback_query(F.data == "send_newsletter")
async def confirm_newsletter(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message = user_data["content"]
    add_newsletter(message.text, message.from_user.id)
    for user in get_all_users():
        if user[0] not in (f[1] for f in getAllBannedUsers()):
            try:
                await message.copy_to(chat_id=user[0])
            except:
                print(f"Не удалось отправить сообщение пользователю с id {user[0]}")
    await call.message.answer(f"Сообщение успешно отправлено")
    await call.message.edit_reply_markup()
    await state.clear()

@admin_private_router.callback_query(F.data == "cancel_newsletter")
async def cancel_newsletter(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отправка сообщения отменена.")
    await call.message.edit_reply_markup()
    await state.clear()

# FAQ
@admin_private_router.message(F.text == "Добавить вопрос в FAQ")
async def start_add_faq(message: types.Message, state: FSMContext):
    await message.answer("Введите группу вопроса:")
    await state.set_state(FAQ_States.waiting_for_question_group)

@admin_private_router.message(FAQ_States.waiting_for_question_group)
async def get_question_group(message: types.Message, state: FSMContext):
    question_group = message.text
    await state.update_data(question_group=question_group)
    await message.answer("Введите вопрос:")
    await state.set_state(FAQ_States.waiting_for_question)

@admin_private_router.message(FAQ_States.waiting_for_question)
async def get_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await message.answer("Введите ответ:")
    await state.set_state(FAQ_States.waiting_for_answer)

@admin_private_router.message(FAQ_States.waiting_for_answer)
async def get_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    add_faq(user_data["question_group"], user_data["question"], answer)
    await message.answer("FAQ успешно добавлен!")
    await state.clear()

#Мероприятия
@admin_private_router.message(F.text == "Добавить мероприятие в календарь")
async def start_add_event(message: types.Message, state: FSMContext):
    await message.answer("Введите название мепроприятия:")
    await state.set_state(Event_States.waiting_for_name)

@admin_private_router.message(Event_States.waiting_for_name)
async def get_event_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Введите дату мероприятия:")
    await state.set_state(Event_States.waiting_for_datetime)

@admin_private_router.message(Event_States.waiting_for_datetime)
async def get_event_date(message: types.Message, state: FSMContext):
    try:
        date_str = message.text
        date = datetime.strptime(date_str, "%d.%m.%Y")
        await state.update_data(date=date)
        user_data = await state.get_data()
        add_event(user_data["name"], user_data["date"].strftime("%Y-%m-%d"))
        await message.answer(f"Дата {date.strftime('%d.%m.%Y')} была сохранена в базе данных.")
        await state.finish()
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате 'дд.мм.гггг'.")
        await state.set_state(Event_States.waiting_for_datetime)

# СОЗДАНИЕ ОПРОСНИКА
@admin_private_router.message(F.text == "Создать опрос")
async def create_quiz(message: types.Message,state: FSMContext):
    await message.answer("Напишите текст вопроса",reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove())
    await state.set_state(Quiz_Creation_States.waiting_for_question)

@admin_private_router.message(Quiz_Creation_States.waiting_for_question)
async def quiz_creation_question(message: types.Message, state: FSMContext):
    await message.answer("Вопрос добавлен")
    await message.answer("Выберите действие на клавиатуре",reply_markup=quiz_keyboard)
    await state.update_data(txt=(f"_q{message.text}_q"))
    await state.set_state(Quiz_Creation_States.waiting_for_actions)
    

@admin_private_router.message(Quiz_Creation_States.waiting_for_actions)
async def quiz_actions(message: types.Message,state:FSMContext):
    if(message.text == "Добавить ответ"):
        await message.answer("Напишите текст ответа",reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove())
        await state.set_state(Quiz_Creation_States.waiting_for_answer)
    elif(message.text == "Закончить создание опроса"):
        send_buttons = [
            [types.KeyboardButton(text="Сделать рассылку опроса")],
            [types.KeyboardButton(text="Отмена")]
        ]

        send_keyboard = types.ReplyKeyboardMarkup(keyboard=send_buttons, resize_keyboard=True)
        await message.answer("Создание опроса успешно завершено. Выберите действие на клавиатуре",reply_markup=send_keyboard)
        await state.set_state(Quiz_Creation_States.waiting_for_send)

@admin_private_router.message(Quiz_Creation_States.waiting_for_answer)
async def quiz_creation_answer(message: types.Message, state:FSMContext):
    await message.answer("Ответ успешно добавлен",reply_markup=quiz_keyboard)
    await message.answer("Выберите действие на клавиатуре")
    st = await state.get_data()
    await state.update_data(txt=st["txt"]+f"{message.text};")
    await state.set_state(Quiz_Creation_States.waiting_for_actions)

@admin_private_router.message(Quiz_Creation_States.waiting_for_send)
async def send_quiz(message: types.Message, state: FSMContext):
    if(message.text=="Отмена"):
        await message.answer("Рассылка опроса успешно отменена",reply_markup=admin_keyboard)
    elif message.text=="Сделать рассылку опроса":
            data = await state.get_data()
            quiz_question = data["txt"].split("_q")[1]
            quiz_answers = data["txt"].split("_q")[2]
            id = add_quiz(quiz_question,quiz_answers)
            answer_buttons = []
            for ans in quiz_answers.split(';'):
                if len(str(ans))>0:
                    answer_buttons.append(types.InlineKeyboardButton(text=str(ans),callback_data=f"quiz_{id}_{str(ans)}"))
            answer_keyboard = types.InlineKeyboardMarkup(inline_keyboard=chunk_list(answer_buttons,1))
            for user in get_all_users():
                if user[0] not in (f[1] for f in getAllBannedUsers()):
                    try: 
                        await bot.send_message(chat_id=user[0],text="📢🚨_Вам пришел новый опрос от Студсовета_\.📪", parse_mode=ParseMode.MARKDOWN_V2)
                        await bot.send_message(chat_id=user[0],text=f"{quiz_question}",reply_markup=answer_keyboard)              
                    except:
                        print(f"Не удалось отправить сообщение пользователю с id {user[0]}")
            await message.answer("Опрос успешно разослан всем пользователям",reply_markup=admin_keyboard)
            await state.clear()
