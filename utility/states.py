from aiogram.fsm.state import StatesGroup, State

class NewsletterStates(StatesGroup):
    waiting_for_subject = State()
    waiting_for_content = State()
    confirm_newsletter = State()

class FAQ_States(StatesGroup):
    waiting_for_question_group = State()
    waiting_for_question = State()
    waiting_for_answer = State()

class Event_States(StatesGroup):
    waiting_for_name = State()
    waiting_for_datetime = State()

class Add_Admin_States(StatesGroup):
    waiting_for_username = State()
    waiting_for_id = State()
    waiting_for_login = State()
    waiting_for_password = State()

class Delete_Admin_States(StatesGroup):
    waiting_for_id = State()

class Ask_Admin_States(StatesGroup):
    waiting_for_question = State()
    waiting_for_reply = State()

class Quiz_Creation_States(StatesGroup):
    waiting_for_question=State()
    waiting_for_answer=State()
    waiting_for_actions = State()
    waiting_for_send=State()