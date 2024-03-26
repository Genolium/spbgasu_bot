import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_db():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (tg_id INTEGER PRIMARY KEY, registration_time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (tg_id INTEGER PRIMARY KEY, username TEXT, login TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS faq
                 (id INTEGER PRIMARY KEY, question_group TEXT, question TEXT, answer TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quizes
                 (id INTEGER PRIMARY KEY, question TEXT, answer_options TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quizes_responces
                 (id INTEGER PRIMARY KEY, tg_id INTEGER, quiz_id INTEGER, answer_number INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY, tg_id INTEGER, request_time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY, name TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS newsletters
                 (id INTEGER PRIMARY KEY, text TEXT, sender_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (id INTEGER PRIMARY KEY, name TEXT, link TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS giveaways
                 (id INTEGER PRIMARY KEY, winners_count INTEGER, result_date TEXT, winner TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS banned_users
                 (id INTEGER PRIMARY KEY, tg_id INTEGER)''')
    conn.commit()
    try:
        c.execute("INSERT INTO admins (tg_id, username, login, password) VALUES (?, ?, ?, ?)", (349646233, "Васюнин И.", "admin", generate_password_hash("AdminPassword222")))
        conn.commit()
    except:
        print("Стандартный логин админа уже добавлен")
    conn.close()

def add_user(tg_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (tg_id, registration_time) VALUES (?, ?)", (tg_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()


def add_faq(question_group, question, answer):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO faq (question_group, question, answer) VALUES (?, ?, ?)", (question_group, question, answer))
    conn.commit()
    conn.close()

def add_quiz(question, answer_options):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO quizes (question, answer_options) VALUES (?, ?)", (question, answer_options))
    quiz_id = c.lastrowid
    conn.commit()
    conn.close()
    return quiz_id

def add_quiz_response(tg_id, quiz_id, answer_number):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO quizes_responces (tg_id, quiz_id, answer_number) VALUES (?, ?, ?)", (tg_id, quiz_id, answer_number))
    conn.commit()
    conn.close()

def add_request(tg_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO requests (tg_id, request_time) VALUES (?, ?)", (tg_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def add_event(name, date):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (name, date) VALUES (?, ?)", (name, date))
    conn.commit()
    conn.close()

def add_newsletter(text, sender_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO newsletters (text, sender_id) VALUES (?, ?)", (text, sender_id))
    conn.commit()
    conn.close()

def add_resource(name, link):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO resources (name, link) VALUES (?, ?)", (name, link))
    conn.commit()
    conn.close()

def add_giveaway(winners_count, result_date, winner):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO giveaways (winners_count, result_date, winner) VALUES (?, ?, ?)", (winners_count, result_date, winner))
    conn.commit()
    conn.close()

def get_all_admins():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins")
    a = list(c.fetchall())
    conn.commit()
    conn.close()
    return a

def add_admin(tg_id, username, login, password):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO admins (tg_id, username, login, password) VALUES (?, ?, ?, ?)", (tg_id, username, login, password))
    conn.commit()
    conn.close()

def delete_admin(tg_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM admins WHERE tg_id = ?", (tg_id,))
    conn.commit()
    conn.close()

def get_pass_hash(login):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT password FROM admins WHERE login = ?", (login,))
    results = c.fetchone()
    conn.close()
    return results

def get_quiz_list():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT id, question FROM quizes")
    quizes = c.fetchall()
    conn.close()
    return quizes

def setBanUser(tg_id, isBanned):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if isBanned:
        c.execute("INSERT INTO banned_users (tg_id) VALUES (?)", (int(tg_id),))
    else:
        c.execute("DELETE FROM banned_users WHERE tg_id = ?", (int(tg_id),))
    conn.commit()
    c.close()
    conn.close()

def getAllBannedUsers():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM banned_users")
    users = c.fetchall()
    conn.close()
    return users

# Функция для получения результатов выбранного опроса
def get_quiz_results(quiz_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT answer_number, COUNT(*) as count FROM quizes_responces WHERE quiz_id = ? GROUP BY answer_number", (quiz_id,))
    results = c.fetchall()
    conn.close()
    return results

def get_quiz_name(quiz_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT question FROM quizes WHERE id = ?", (quiz_id,))
    name = c.fetchone()[0]
    conn.close()
    return name

def get_all_users():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    a = list(c.fetchall())
    conn.commit()
    conn.close()
    return a

def get_user(tg_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
    a = c.fetchone()
    conn.commit()
    conn.close()
    return a

def get_faq(question_group=None, question=None, id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if question_group and question:
        c.execute("SELECT * FROM faq WHERE question_group = ? AND question = ?", (question_group, question))
    elif id:
        c.execute("SELECT * FROM faq WHERE id = ?", (id,))
    elif question_group:
        c.execute("SELECT * FROM faq WHERE question_group = ?", (question_group,))
    elif question:
        c.execute("SELECT * FROM faq WHERE question = ?", (question,))
    else:
        c.execute("SELECT * FROM faq")
        faq_data = {}
        for row in c.fetchall():
            id, question_group, question, answer = row
            if question_group not in faq_data:
                faq_data[question_group] = {}
            faq_data[question_group][question] = answer

        conn.commit()
        conn.close()
        return faq_data
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_quiz(quiz_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if quiz_id:
        c.execute("SELECT * FROM quizes WHERE id = ?", (quiz_id,))
    else:
        c.execute("SELECT * FROM quizes")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_quizes_responces(tg_id=None, quiz_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if tg_id and quiz_id:
        c.execute("SELECT * FROM quizes_responces WHERE tg_id = ? AND quiz_id = ?", (tg_id, quiz_id))
    elif tg_id:
        c.execute("SELECT * FROM quizes_responces WHERE tg_id = ?", (tg_id,))
    elif quiz_id:
        c.execute("SELECT * FROM quizes_responces WHERE quiz_id = ?", (quiz_id,))
    else:
        c.execute("SELECT * FROM quizes_responces")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_request(tg_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if tg_id:
        c.execute("SELECT * FROM requests WHERE tg_id = ?", (tg_id,))
    else:
        c.execute("SELECT * FROM requests")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_event(event_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if event_id:
        c.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    else:
        c.execute("SELECT * FROM events")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_newsletter(newsletter_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if newsletter_id:
        c.execute("SELECT * FROM newsletters WHERE id = ?", (newsletter_id,))
    else:
        c.execute("SELECT * FROM newsletters")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_resource(resource_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if resource_id:
        c.execute("SELECT * FROM resources WHERE id = ?", (resource_id,))
    else:
        c.execute("SELECT * FROM resources")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def get_giveaway(giveaway_id=None):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    if giveaway_id:
        c.execute("SELECT * FROM giveaways WHERE id = ?", (giveaway_id,))
    else:
        c.execute("SELECT * FROM giveaways")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def edit_faq(faq_id, question_group, question, answer):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("UPDATE faq SET question_group = ?, question = ?, answer = ? WHERE id = ?", (question_group, question, answer, faq_id))
    conn.commit()
    conn.close()

def delete_faq(question_group, question):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM faq WHERE question_group = ? AND question = ?", (question_group, question))
    conn.commit()
    conn.close()

def edit_quiz(quiz_id, question, answer_options):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("UPDATE quizes SET question = ?, answer_options = ? WHERE id = ?", (question, answer_options, quiz_id))
    conn.commit()
    conn.close()

def delete_quiz(quiz_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM quizes WHERE id = ?", (quiz_id,))
    conn.commit()
    conn.close()

def edit_event(event_id, name, date):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("UPDATE events SET name = ?, date = ? WHERE id = ?", (name, date, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def edit_resource(resource_id, name, link):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("UPDATE resources SET name = ?, link = ? WHERE id = ?", (name, link, resource_id))
    conn.commit()
    conn.close()

def delete_resource(resource_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
    conn.commit()
    conn.close()

def isAdmin(user_id):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE id = ?", (user_id,))
    if len(c.fetchone())>0:
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False
    
# Функции для работы с базой данных
def get_faq_groups():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT question_group FROM faq")
    groups = [row[0] for row in c.fetchall()]
    conn.close()
    return groups

def get_faq_by_group(group):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM faq WHERE question_group = ?", (group,))
    faq_items = c.fetchall()
    conn.close()
    return faq_items