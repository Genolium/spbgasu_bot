from flask import Flask, Response, render_template, request, redirect, url_for, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from utility.db import *
from utility.util import *

# СОЗДАНИЕ ВЕБ-ПРИЛОЖЕНИЯ НА FLASK
app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in (i[2] for i in get_all_admins()) and check_password_hash(str(get_pass_hash(username)[0]), password):
        return username

@app.route('/')
@auth.login_required(optional=True)
def index():
    a = auth.current_user()
    if a!=None:
        return render_template('index.html', username=a)
    else:
        return render_template('index.html', username="anonymous")

@app.route('/users', methods=['GET', 'POST'])
@auth.login_required
def users():    
    users_list = get_all_users()
    banned_users = getAllBannedUsers()  
    return render_template('users.html', users=users_list, banned_users=list((f[1] for f in banned_users)))

@app.route('/faq', methods=['GET', 'POST'])
@auth.login_required
def faq():
    if request.method == 'POST':
        question_group = request.form['question_group']
        question = request.form['question']
        answer = request.form['answer']
        add_faq(question_group, question, answer)
        return redirect(url_for('faq'))

    faq_list = get_faq()
    full_list = get_faq(id=-1)
    print(full_list)
    l = dict()
    for i in full_list:
        l[i[2]]=i[0]
    return render_template('faq.html', faq=faq_list, flist=l)

@app.route('/faq/delete', methods=['GET'])
@auth.login_required
def deletefaq():
    question_group = request.args.get('question_group')
    question = request.args.get('question')
    delete_faq(question_group, question)
    return redirect(url_for('faq'))

@app.route('/admin_management', methods=['GET', 'POST'])
@auth.login_required
def admin_management():
    if request.method == 'POST':
        if 'add_admin' in request.form:
            tg_id = request.form['tg_id']
            username = request.form['username']
            login = request.form['login']
            password = generate_password_hash(request.form['password'])
            add_admin(tg_id, username, login, password)
        elif 'delete_admin' in request.form:
            tg_id = request.form['tg_id']
            delete_admin((tg_id,))
    admins = get_all_admins()
    return render_template('admin_management.html', admins=admins)

# Главная страница со списком событий и формой для добавления/редактирования
@app.route('/events', methods=['GET', 'POST'])
@auth.login_required
def events():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        event_id = request.form['event_id']        
        
        if event_id:
            # Обновление существующего события
            edit_event(event_id, name, date)
        else:
            add_event(name,date)
        return redirect('/events')
    events = get_event()
    return render_template('events.html', events=events)

# Удаление события по id
@app.route('/events/delete/<int:event_id>', methods=['POST'])
@auth.login_required
def del_event(event_id):  
    delete_event(event_id)  
    return redirect('/events')

@app.route('/quiz', methods=['GET', 'POST'])
@auth.login_required
def quiz():
    if request.method == 'POST':
        # Получаем выбранный опрос из формы
        selected_quiz = int(request.form['quiz'])
        quiz_results = get_quiz_results(selected_quiz)
        chart = generate_chart(quiz_results)
        quiz_name = get_quiz_name(selected_quiz)
        people = sum(list(row[1] for row in quiz_results))
        return render_template('quiz.html', chart=chart, quiz_name=quiz_name, people=people)
    else:
        # Получаем список опросов
        quiz_list = get_quiz_list()
        return render_template('quiz.html', quiz_list=quiz_list)
    
@app.route('/ban_user/<tg_id>', methods=['POST'])
@auth.login_required
def ban_user(tg_id):
    setBanUser(tg_id, True)
    return redirect('/users')

@app.route('/unban_user/<tg_id>', methods=['POST'])
@auth.login_required
def unban_user(tg_id):
    setBanUser(tg_id, False)
    return redirect('/users')

@auth.login_required
@app.route('/logout')
def logout():
    response = make_response('Logout Successful', 401)
    response.headers['Location'] = '/'  # Устанавливаем заголовок Location для редиректа
    return response

@app.route('/faq/edit/', methods=['GET', 'POST'])
@auth.login_required
def editfaq():
    if request.method == 'POST':
        id = request.args.get('id')
        question_group = request.form['question_group']
        question = request.form['question']
        answer = request.form['answer']
        edit_faq(id,question_group, question, answer)
        return redirect(url_for('faq'))

    question_group = request.args.get('question_group')
    question = request.args.get('question')
    answer = request.args.get('answer')
    return render_template('faq_edit.html', question_group=question_group, question=question, answer=answer)

@app.route('/events/edit/', methods=['GET', 'POST'])
@auth.login_required
def editevent():
    id = request.args.get('id')
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        edit_event(id,name,date)
        return redirect(url_for('events'))
    return render_template('event_edit.html', event=get_event(id))