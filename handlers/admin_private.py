#           ОБРАБОТКА АДМИНСКИХ КОМАНД
from aiogram import types,Router,F,flags
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode
from werkzeug.security import generate_password_hash
from filters.is_admin import IsAdminIDFilter
from keyboardrs.admin_keyboards import *
from keyboardrs.quiz_create_keyboard import quiz_keyboard
from keyboardrs.advanced_admin import advanced_keyboard
from utility.util import *
from utility.db import *
from utility.states import *

admin_private_router=Router()
admin_private_router.message.filter(IsAdminIDFilter())

# ПРИВЕТСТВИЕ
@admin_private_router.message(CommandStart())
@flags.chat_action(action="typing")
async def start_cmd(message: types.Message, command: CommandObject, state:FSMContext):
    await state.clear()
    args = command.args
    if args and int(args):
        a = int(args)
        button_url = f'tg://user?id={a}'
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Ссылка", url=button_url)]])
        await bot.send_message(message.chat.id, text=f'🔗👇Ссылка на id {a}:\n\n<a href="tg://user?id={a}">ссылка</a>', reply_markup=markup, parse_mode=ParseMode.HTML)
    elif not get_user(message.from_user.id):
       add_user(message.from_user.id)
    await message.answer(F'Добрый день,<b>администратор {message.from_user.username}</b>👋',reply_markup=admin_keyboard, parse_mode=ParseMode.HTML)

# ВЫВОД СПИСКА АДМИНОВ
@admin_private_router.message(F.text == "📋Список администраторов")
@flags.chat_action(action="typing")
async def admin_list(message: types.Message, state:FSMContext):
    await state.clear()
    l = ""
    for admin in get_all_admins():
        id = str(admin[0])
        user = admin[1]
        l += f"{user}: id={id}\n"
    await message.answer(l)

# ДОБАВЛЕНИЕ АДМИНА 
@admin_private_router.message(F.text == "📝Добавить администратора")
async def add_admin_message(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✍️Введите *имя* нового *администратора*\.",reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Add_Admin_States.waiting_for_username)

@admin_private_router.message(Add_Admin_States.waiting_for_username)
async def add_admin_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("✍️Введите *id* для нового *администратора*\(его можно узнать с помощью команды /id в боте\)\.", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Add_Admin_States.waiting_for_id)

@admin_private_router.message(Add_Admin_States.waiting_for_id)
async def add_admin_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.reply("✍️Введите *логин* для нового *администратора*\.", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Add_Admin_States.waiting_for_login)
    
@admin_private_router.message(Add_Admin_States.waiting_for_login)
async def add_admin_username(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.reply("✍️Введите пароль для нового *администратора*\.", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Add_Admin_States.waiting_for_password)

@admin_private_router.message(Add_Admin_States.waiting_for_password)
async def add_admin_username(message: types.Message, state: FSMContext):
    try:
        await state.update_data(password=message.text)
        new_admin_data = await state.get_data()
        add_admin(int(new_admin_data["id"]), str(new_admin_data["username"]), str(new_admin_data["login"]), str(generate_password_hash(new_admin_data["password"])))    
        await message.reply("✅Новый *администратор успешно добавлен*\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
    except:
        await message.reply("❌*Не удалось* добавить администратора\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()

# УДАЛЕНИЕ АДМИНА ПО ID
@admin_private_router.message(F.text == "🗑️Удалить администратора по id")
async def delete_admin_message(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✍️Введите *Telegram ID администратора*, которого нужно удалить\.", reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(),parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Delete_Admin_States.waiting_for_id)

@admin_private_router.message(Delete_Admin_States.waiting_for_id)
async def delete_admin_id(message: types.Message, state: FSMContext):
    try:
        tg_id = message.text
        delete_admin(int(tg_id))
        await message.reply("✅Администратор *успешно* удален\.", reply_markup=advanced_keyboard,parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
    except:
        await message.reply("❌*Не удалось* удалить администратора\.", reply_markup=advanced_keyboard,parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()

# РАССЫЛКИ
@admin_private_router.message(F.text == "📨Создать рассылку")
async def send_newsletter(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [types.KeyboardButton(text="Отмена")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('''Напишите текст *рассылки* 📩, который будет отправлен *всем пользователям* бота 🤖\n
Вы можете *использовать оформление из Telegram* \(жирный текст, курсив, спойлер и т\.д\.\)''',reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(NewsletterStates.waiting_for_content)

@admin_private_router.message(NewsletterStates.waiting_for_content)
async def get_newsletter_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message)

    if message.text and message.text.lower()=="отмена":
        await message.answer("✅Создание рассылки *отменено*\.", parse_mode=ParseMode.MARKDOWN_V2,reply_markup=admin_keyboard)
        await state.clear()
    else:     
        keyboard = types.InlineKeyboardMarkup(row_width=2,inline_keyboard=[
            [
                types.InlineKeyboardButton(text="✅Отправить рассылку", callback_data="send_newsletter"),
                types.InlineKeyboardButton(text="❌Отмена", callback_data="cancel_newsletter")
            ]
        ])
        await message.answer(f"⚠️Пожалуйста,подтвердите отправку сообщения👇", reply_markup=keyboard)
        await state.set_state(NewsletterStates.confirm_newsletter)

@admin_private_router.callback_query(F.data == "send_newsletter")
@flags.chat_action(action="typing")
async def confirm_newsletter(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message = user_data["content"]
    add_newsletter(message.text, message.from_user.id)
    for user in get_all_users():
        if user[0] not in (f[1] for f in getAllBannedUsers()):
            try:
                await message.copy_to(chat_id=user[0])
            except:
                print(f"❌Не удалось отправить сообщение пользователю с id {user[0]}")
    await call.message.answer(f"✅*Сообщение успешно отправлено*\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    await call.message.edit_reply_markup()
    await state.clear()

@admin_private_router.callback_query(F.data == "cancel_newsletter")
async def cancel_newsletter(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("❌*Отправка сообщения отменена*\.", parse_mode=ParseMode.MARKDOWN_V2,reply_markup=admin_keyboard)
    await call.message.edit_reply_markup()
    await state.clear()

# FAQ
@admin_private_router.message(F.text == "📌❓Добавить вопрос в FAQ📝")
async def start_add_faq(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✍️Введите *раздел* вопроса:",reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(FAQ_States.waiting_for_question_group)

@admin_private_router.message(FAQ_States.waiting_for_question_group)
async def get_question_group(message: types.Message, state: FSMContext):
    question_group = message.text
    await state.update_data(question_group=question_group)
    await message.answer("✍️Введите *вопрос*:", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(FAQ_States.waiting_for_question)

@admin_private_router.message(FAQ_States.waiting_for_question)
async def get_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await message.answer("✍️Введите *ответ*:", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(FAQ_States.waiting_for_answer)

@admin_private_router.message(FAQ_States.waiting_for_answer)
async def get_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_data = await state.get_data()
    add_faq(user_data["question_group"], user_data["question"], answer)
    await message.answer("✅*FAQ* успешно добавлен\!", reply_markup=advanced_keyboard,parse_mode=ParseMode.MARKDOWN_V2)
    await state.clear()

#Мероприятия
@admin_private_router.message(F.text == "📅🖋️Добавить мероприятие в календарь")
async def start_add_event(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✍️Введите *название* мероприятия\:", reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(),parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Event_States.waiting_for_name)

@admin_private_router.message(Event_States.waiting_for_name)
async def get_event_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("📷Пришлите *фото* для обложки мероприятия\:", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Event_States.waiting_for_photo)

@admin_private_router.message(Event_States.waiting_for_photo, F.content_type == types.ContentType.PHOTO)
async def get_event_name(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(photo=photo)
    await state.update_data(file_id=file_id)
    await message.answer("✍️Введите *дату* мероприятия\:", parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Event_States.waiting_for_datetime)

@admin_private_router.message(Event_States.waiting_for_datetime)
async def get_event_date(message: types.Message, state: FSMContext):
    try:
        date_str = message.text
        await state.update_data(date=date_str)
        await message.answer("✍️Введите *описание* мероприятия\:",parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Event_States.waiting_for_description)
    except ValueError:
        await message.answer("❌*Неверный формат*", parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Event_States.waiting_for_datetime)

@admin_private_router.message(Event_States.waiting_for_description)
async def get_event_date(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    user_data = await state.get_data()
    add_event(user_data["name"],user_data["date"],user_data["description"], user_data["file_id"])
    await message.answer(f"✅Описание было сохранено в базе данных.",reply_markup=advanced_keyboard)
    await state.clear()

# СОЗДАНИЕ ОПРОСНИКА
@admin_private_router.message(F.text == "🗳️Создать опрос")
async def create_quiz(message: types.Message,state: FSMContext):
    await state.clear()
    kb = [
        [types.KeyboardButton(text="❌Отмена")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("✍️Напишите *вопрос*\.\n\nЧтобы *отменить* создание опроса, нажмите *❌Отмена*\.",
                         reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Quiz_Creation_States.waiting_for_question)

@admin_private_router.message(Quiz_Creation_States.waiting_for_question)
async def quiz_creation_question(message: types.Message, state: FSMContext):
    if message.text.lower()=="❌отмена":
        await message.answer("✅Создание опроса *отменено*\.", parse_mode=ParseMode.MARKDOWN_V2,reply_markup=admin_keyboard)
        await state.clear()
    else:
        await message.answer("✅Вопрос *добавлен*\.", parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer("👉*Выберите действие* на клавиатуре⌨️\.",reply_markup=quiz_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Quiz_Creation_States.waiting_for_actions)
        st = await state.get_data()
        try:
            await state.update_data(txt=(st["txt"]+f"_q{message.text}_q"))    
        except:
            await state.update_data(txt=(f"{message.text}_q"))
        

@admin_private_router.message(Quiz_Creation_States.waiting_for_actions)
async def quiz_actions(message: types.Message,state:FSMContext):
    if(message.text == "📝Добавить ответ"):
        await message.answer("✍️*Напишите* текст ответа\.",reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Quiz_Creation_States.waiting_for_answer)
    elif(message.text == "Закончить создание опроса🔚"):
        send_buttons = [
            [types.KeyboardButton(text="📢Сделать рассылку опроса")],
            [types.KeyboardButton(text="❌Отмена")]
        ]

        send_keyboard = types.ReplyKeyboardMarkup(keyboard=send_buttons, resize_keyboard=True)
        await message.answer("✅Создание опроса *успешно завершено*\. Выберите действие на клавиатуре⌨️\.",reply_markup=send_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Quiz_Creation_States.waiting_for_send)
    elif(message.text=="📝Добавить новый вопрос"):
        await message.answer("✍️Напишите *вопрос*\.",
            reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Quiz_Creation_States.waiting_for_question)

@admin_private_router.message(Quiz_Creation_States.waiting_for_answer)
async def quiz_creation_answer(message: types.Message, state:FSMContext):
    if ';' in message.text:
        await message.answer("❌Отмена в ответе нельзя использовать символ ;")
    else:
        await message.answer("✅Ответ *успешно* добавлен\.",reply_markup=quiz_keyboard, parse_mode=ParseMode.MARKDOWN_V2 )
        await message.answer("Выберите *действие* на клавиатуре⌨️", parse_mode=ParseMode.MARKDOWN_V2)
        st = await state.get_data()
        await state.update_data(txt=st["txt"]+f"{message.text};")
        await state.set_state(Quiz_Creation_States.waiting_for_actions)

@admin_private_router.message(Quiz_Creation_States.waiting_for_send)
@flags.chat_action(action="typing")
async def send_quiz(message: types.Message, state: FSMContext):
    if(message.text=="❌Отмена"):
        await message.answer("✅Рассылка опроса *успешно* отменена\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    elif message.text=="📢Сделать рассылку опроса":
            data = await state.get_data()
            data_array = data["txt"].split("_q")
            quiz_id = get_last_quiz()[0]+1
            quiz_questions=[]
            quiz_answers = []
            for i in range(0,len(data["txt"].split("_q"))):
                if i % 2 !=0:
                    #data_array[i-1] текст вопроса
                    #data_array[i] варианты ответа на вопрос
                    quiz_questions.append(data_array[i-1])
                    quiz_answers.append(data_array[i])
                    add_quiz(quiz_id,data_array[i-1],data_array[i])
           
            answer_buttons = []
            for ans in data_array[1].split(';'):
                if len(str(ans))>0:
                    if(len(data_array)==2):#Если в опросе всего один вопрос
                        answer_buttons.append(types.InlineKeyboardButton(text=str(ans),callback_data=f"quiz_{quiz_id}_{str(ans)}"))
                    else:
                        answer_buttons.append(types.InlineKeyboardButton(text=str(ans),callback_data=f"quiz_{quiz_id}_{str(ans)}_0_{len(quiz_questions)}"))
            answer_keyboard = types.InlineKeyboardMarkup(inline_keyboard=chunk_list(answer_buttons,1))
            for user in get_all_users():
                if user[0] not in (f[1] for f in getAllBannedUsers()):
                    try: 
                        await bot.send_message(chat_id=user[0],text="📢🚨_Вам пришел новый опрос от Студсовета_\.📪", parse_mode=ParseMode.MARKDOWN_V2)
                        await bot.send_message(chat_id=user[0],text=f"{quiz_questions[0]}",reply_markup=answer_keyboard)              
                    except:
                        message.answer(f"❌*Не удалось отправить* сообщение пользователю с id {user[0]}\.", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer("✅Опрос *успешно* разослан всем пользователям\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
            await state.clear()

# РАСШИРЕННЫЕ НАСТРОЙКИ
@admin_private_router.message(F.text == "⚙️Расширенные настройки")
async def advanced_options(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("👉Вы *перешли* в расширенные настройки\.",reply_markup=advanced_keyboard, parse_mode=ParseMode.MARKDOWN_V2)
# ВЫХОД ИЗ РАСШИРЕННЫХ НАСТРОЕК    
@admin_private_router.message(F.text == "⏪")
async def advanced_options(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("👉Вы *вышли* из расширенных настроек\.",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)

# РЕЖИМ ПОЛЬЗОВАТЕЛЯ
@admin_private_router.message(F.text == "🫥Режим пользователя")
async def advanced_options(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("👉Вы *перешли* в режим простого пользователя\.",reply_markup=fake_user_keyboard, parse_mode=ParseMode.MARKDOWN_V2)

# ВЫХОД ИЗ РЕЖИМА ПОЛЬЗОВАТЕЛЯ    
@admin_private_router.message(F.text == "Вернуться⏪")
async def advanced_options(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("👉Вы *вышли* из режима простого пользователя\. Поздравляем с возвращением\!",reply_markup=admin_keyboard, parse_mode=ParseMode.MARKDOWN_V2)

#Изменение фото в мероприятии
@admin_private_router.message(F.text == "🖋️🎥Изменить фото в мероприятии")
async def change_photo_1(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("📷Введите id мероприятия, у которого вы хотите изменить обложку\:",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[cancel_button], resize_keyboard=True),parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Change_Photo_States.waiting_for_num)

@admin_private_router.message(Change_Photo_States.waiting_for_num)
async def change_photo_2(message: types.Message, state: FSMContext):
    await state.clear()
    if message.text == "⏪ Отменить":
        await message.answer(f"Изменение обложки отменено",reply_markup=advanced_keyboard)
        await state.clear()
        return
    event = get_event(message.text)
    if event:
        event = event[0]
        await state.update_data(id=message.text)
        await message.answer(f"Вы решили изменить обложку для мероприятия: \n\n<b>Название:</b> {event[1]}\n<b>Дата:</b> {event[2]}\n<b>Описание:</b> {event[3]}",
                             parse_mode=ParseMode.HTML)
        await message.answer("📷Пришлите новое *фото* для обложки мероприятия\. \n\nЕсли вы хотите убрать обложку мепоприятия, нажмите на кнопку внизу",
            reply_markup=types.ReplyKeyboardMarkup(keyboard=[cancel_button, remove_photo_button], resize_keyboard=True), parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Change_Photo_States.waiting_for_new_photo)
    else:
        await message.answer(f"Похоже, мероприятия с таким Id не существует. Повторите ввод")

@admin_private_router.message(Change_Photo_States.waiting_for_new_photo,F.content_type == types.ContentType.PHOTO)
async def change_photo_3(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    user_data = await state.get_data()
    id=user_data["id"]
    event = get_event(id)[0]
    edit_event(event[0],event[1],event[2],event[3],file_id)
    await message.answer(f"✅Фото мероприятия было обновлено.",reply_markup=advanced_keyboard)
    await state.clear()
    
@admin_private_router.message(Change_Photo_States.waiting_for_new_photo,F.content_type == types.ContentType.TEXT)
async def change_photo_3(message: types.Message, state: FSMContext):
    if message.text=="❗️Убрать обложку❗️":
        user_data = await state.get_data()
        id=user_data["id"]
        event = get_event(id)[0]
        edit_event(event[0],event[1],event[2],event[3],None)
        await message.answer(f"✅Обложка мероприятия была удалена!",reply_markup=advanced_keyboard)
        await state.clear()
    if message.text == "⏪ Отменить":
        await message.answer(f"Изменение обложки отменено",reply_markup=advanced_keyboard)
        await state.clear()
    
#ОТКРЫТЬ САЙТ
@admin_private_router.message(F.text == "☁️Открыть сайт")
async def open_website(message: types.Message, state:FSMContext):
    link_button = types.InlineKeyboardButton(text='🔗Ссылка', url=FLASK_SITE_ADDRESS)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[link_button]])
    await message.answer('Нажми на кнопку, чтобы перейти по ссылке', reply_markup=keyboard)

#ИЗМЕНЕНИЕ УЧЁТКИ
@admin_private_router.message(F.text == "🖋️Изменить свои учетные данные")
async def change_password(message: types.Message, state:FSMContext):
    await message.answer('Введите новый логин (для отмены нажмите на кнопку внизу)', reply_markup=types.ReplyKeyboardMarkup(keyboard=[cancel_button], resize_keyboard=True))
    await state.set_state(ChangeCredentials.waiting_for_login)

@admin_private_router.message(ChangeCredentials.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    if message.text == "⏪ Отменить":
        await message.answer(f"Изменение учетных данных отменено",reply_markup=advanced_keyboard)
        await state.clear()
    else:
        login = message.text
        await state.update_data(login=login)
        await message.answer('Введите новый пароль (для выхода нажмите на кнопку внизу)', reply_markup=types.ReplyKeyboardMarkup(keyboard=[cancel_button], resize_keyboard=True))
        await state.set_state(ChangeCredentials.waiting_for_password)

@admin_private_router.message(ChangeCredentials.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    if message.text == "⏪ Отменить":
        await message.answer(f"Изменение учетных данных отменено",reply_markup=advanced_keyboard)
        await state.clear()
    else:
        password = message.text
        data = await state.get_data()
        login = data.get('login')
        tg_id = message.from_user.id
        edit_admin(tg_id, login, password)
        await message.answer('Ваши учетные данные успешно обновлены!',reply_markup=advanced_keyboard)
        await state.clear()