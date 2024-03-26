#           ОБРАБОТКА ПОЛЬЗОВАТЕЛЬСКИХ КОМАНД
from aiogram import types,Router,F,flags
from aiogram.filters import Command,CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from utility.db import *
from utility.util import *
from utility.states import *
from os import getenv
from dotenv import find_dotenv, load_dotenv
from keyboardrs.usr_keyboards import *

user_router = Router()

@user_router.message(CommandStart())
@flags.chat_action(action="upload_photo", interval=3)
async def cmd_start(message: types.Message):
    image = FSInputFile("static/Post.jpg")
    if not get_user(message.from_user.id):
       add_user(message.from_user.id)
    await message.answer_photo(photo=image, caption=f'''👋Привет, *{message.from_user.first_name}*, я бот 🤖 *Студенческого совета университета CПбГАСУ*🏫\n\nМоя основная *цель* \- адаптировать студентов 👨‍🎓👩‍🎓 к жизни в вузе и помочь начать активно учавствовать в ней\.\n
С помощью меня ты можешь:
🗣 Задавать интересующие тебя вопросы;
🙋🙋‍♂️ Учавствовать в различных  опросах;
🤝 Узнавать  даты важных событий/мероприятий вуза;

Пожалуйста, *не стесняйся спрашивать*, я с радостью отвечу 💭 на твои вопросы 🤔, если же ты не можешь найти ответа, пиши обращение 📨 в студенческий совет, тебе обязательно помогут\.'''
,reply_markup=main_keyboard, parse_mode=ParseMode.MARKDOWN_V2)



# КАЛЕНДАРЬ МЕРОПРИЯТИЙ
@user_router.message(F.text=='Календарь мероприятий🗓️')
async def buy_list(message: types.Message):
    image = FSInputFile("static/Events.jpg")
    events = get_event()
    res = ""
    for event in events:
        res += f"{event[1]} - {event[2]}\n"
    await message.answer_photo(photo=image, caption='🗓️📢 *Календарь* содержит даты и названия ближайших *событий/мероприятий* вуза 🏫\.\nДля подробной информации выбирай ниже👇\n\n'+res.replace('.','\.').replace('-','\-'), parse_mode=ParseMode.MARKDOWN_V2)

# ID    
@user_router.message(Command('id'))
async def print_usr_id(message: types.Message):
    await message.answer(f"{message.from_user.id}")

# НАПИСАТЬ ОБРАЩЕНИЕ В СТУДСОВЕТ
@user_router.message(F.text == "Написать обращение в студсовет✍")
async def message_to_admins(message: types.Message,state: FSMContext):
    cancel_button = [
        [types.KeyboardButton(text="Отмена")],
    ]
    cancel_keyboard = types.ReplyKeyboardMarkup(keyboard=cancel_button, resize_keyboard=True)
    image = FSInputFile("static/Respond.jpg")
    await message.answer_photo(photo=image, caption="📝Задайте свой вопрос, пожалуйста *описывайте вопрос/проблему подробно*, вам постараются ответить, как можно быстрее 👩‍💻🧑‍💻\.",parse_mode=ParseMode.MARKDOWN_V2, reply_markup=cancel_keyboard)
    await state.set_state(Ask_Admin_States.waiting_for_question)

@user_router.message(Ask_Admin_States.waiting_for_question)
async def forward_message_to_admins(message: types.Message, state: FSMContext):
    if(message.text == "Отмена"):
        await message.answer("❌Отправка сообщения *отменена*\.",parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_keyboard)
        await state.clear()
    else: 
        load_dotenv(find_dotenv())
        a = message.from_user.id
        button_url = f'tg://user?id={a}'
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Ссылка", url=button_url)]])
        await bot.send_message(chat_id=getenv("ADMIN_GROUP_ID"),text=f"Новое сообщение от пользователя с id {message.from_user.id}\nСсылка на id {a}: <a href='tg://user?id={a}'>ссылка</a>", parse_mode=ParseMode.HTML)
        await message.forward(getenv('ADMIN_GROUP_ID'))
        await state.set_state(Ask_Admin_States.waiting_for_reply)
        await state.update_data(original_message=message)
        await message.answer("✅*Сообщение успешно отправлено* в Студенческий совет и уже обрабатывается, время ответа зависит от количества заявок\.",parse_mode=ParseMode.MARKDOWN_V2, reply_markup=main_keyboard)


# Получение списка групп вопросов FAQ
@user_router.message(F.text=='FAQ📋')
async def show_faq_groups(message: types.Message):
    groups = get_faq_groups()
    buttons = [] 
    for group in groups:
        buttons.append(types.InlineKeyboardButton(text=group, callback_data=f'faq_{group}'))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=chunk_list(buttons,2))
    image = FSInputFile("static/FAQ.jpg")
    await message.answer_photo(photo=image, caption='В разделе *FAQ*, собраны часто задаваемые вопросы студентов,выбери интересующий тебя раздел\n\n👇Выбери раздел вопросов:',parse_mode=ParseMode.MARKDOWN_V2,reply_markup=keyboard)

@user_router.callback_query(F.data.startswith('faq_'))
async def show_faq_questions(call: types.CallbackQuery):
    data = call.data.split('_')
    if len(data)==2:
        if data[1] == 'back':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            group_name = data[1]
            questions = get_faq(question_group=group_name)
            buttons = []
            answer = ""
            c=1
            for question in questions:
                answer += "<b>" + str(c) + '.</b> ' + question[2] + '\n\n'
                buttons.append(types.InlineKeyboardButton(text=str(c), callback_data=f'faq_{group_name}_{question[0]}'))
                c+=1
            buttons.append(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='faq_back'))
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=chunk_list(buttons,2))
            if call.message.text:
                await call.message.edit_text(f'👇<b>Вопросы из раздела "{group_name}</b>": \n\n'+answer, parse_mode=ParseMode.HTML, reply_markup=keyboard)
            else:
                await call.message.answer(f'👇<b>Вопросы из раздела "{group_name}</b>": \n\n'+answer, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    elif len(data)==3:
        q = data[2]
        question = get_faq(id=q)
        if call.message.text:
            await call.message.edit_text(f'👉Ответ на вопрос: "{question[0][2]}"\n\n{question[0][3]}')
        else:
            await call.message.answer(f'👉Ответ на вопрос: "{question[0][2]}"\n\n{question[0][3]}')
        buttons = [
            types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'faq_{data[1]}')
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=chunk_list(buttons,2))
        if call.message.text:
            await call.message.edit_reply_markup(reply_markup=keyboard)
        else:
            await call.message.answer(reply_markup=keyboard)

@user_router.message(F.text=='Наши контакты📞')
async def contact_list(message: types.Message):
    image = FSInputFile("static/Nets.jpg")
    buttons = []
    buttons.append(types.InlineKeyboardButton(text = '🅱Контакте', url="https://vk.com/ssspbgasu"))
    buttons.append(types.InlineKeyboardButton(text = '✉️Telegram', url="https://t.me/studsovetgasu"))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer_photo(photo=image, reply_markup = keyboard)

# ОТВЕТ НА ОПРОСНИК
@user_router.callback_query(F.data.startswith("quiz_"))
async def send_response(call: types.CallbackQuery):
    data = call.data.split("_")
    add_quiz_response(call.from_user.id,data[1],data[2])
    await call.message.edit_reply_markup()
    await call.message.answer("Спасибо за ваш ответ!😊")