from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from flask import Flask, flash, redirect, render_template, request
from models import Employee, FlexStatus, load_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
import math


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile_page():
    user = current_user
    flx = FlexStatus.query.order_by(desc(FlexStatus.enterTime)).filter_by(
        employee_id=current_user.id).first().get_status()

    return render_template('profile.html', user=user, flex=flx)


@app.route('/home', methods=['POST', 'GET'])
def home():
    now = datetime.now()
    week_day = datetime.now().weekday()
    today = {
        'today_date': datetime.now(),
        'week_day': ['Mon', 'Tue', 'Wen', 'Thur', 'Fri', 'Sat', 'Sun'][week_day]
    }
    flxs = FlexStatus.query.filter_by(employee_id=current_user.id).all()
    days = []
    for flx in flxs:
        if flx.enterTime.date() == now.date():
            days.append((flx.enterTime, flx.exitTime))
    if len(days) == 0:
        day_activity = {}
    else:
        day = max(days)
        work_time = (now - day[0]) if day[1] == datetime(1, 1, 1, 1, 1) else (day[1] - day[0])

        day_activity = {
            'daily_activity': f'{(work_time.seconds / 28800) * 100:.2f}',
            'worked_time': f'{work_time.seconds // 3600:02d}:{work_time.seconds // 60 % 60:02d}',
            'hours_remained': f'{(8 - math.ceil(work_time.seconds / 3600)):02d}:{(60 - work_time.seconds // 60 % 60):02d}'

        }

    return render_template('dashboard.html',
                           today=today,
                           user=current_user, day_activity=day_activity)


@app.route('/', methods=['POST', 'GET'])
def login_page():
    login_id = request.form.get('id')
    password = request.form.get('password')

    if login_id and password:
        user = Employee.query.filter_by(login_id=login_id).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect('/home')
        else:
            flash('Password or login is incorrect ')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    if request.method == 'POST':
        login_id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        surname = request.form.get('surname')
        profession = request.form.get('profession')
        rep_password = request.form.get('repeat_password')
        if rep_password == password:
            hash_password = generate_password_hash(password)
            emp = Employee(login_id=login_id, name=name, password=hash_password, surname=surname, profession=profession)
            db.session.add(emp)
            db.session.commit()
            login_user(emp)

            return redirect('/home')
        else:
            pass

    return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_route():
    user_id = current_user.id
    flx_s = FlexStatus.query.filter_by(employee_id=user_id).all()
    today_date = []
    for flx in flx_s:
        if flx.enterTime.date() == datetime.now().date() and flx.exitTime == datetime(1, 1, 1, 1, 1):
            today_date.append((flx.enterTime, flx))
    if len(today_date):
        flx = max(today_date)[1]
        flx.exitTime = datetime.now()
        db.session.commit()
    logout_user()
    return redirect('/')


@app.route('/reset-password', methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        login_id = request.form.get('id')
        name = request.form.get('name')
        surname = request.form.get('surname')
        profession = request.form.get('profession')
        password = request.form.get('password')
        update_employee = Employee.query.filter_by(login_id=login_id).first()

        if name == update_employee.name and surname == update_employee.surname and update_employee.profession == profession:
            update_employee.password = generate_password_hash(password)
            flash('Successfully changed')
            db.session.commit()
            return redirect('/')

    return render_template('reset.html')


@app.route('/work_days')
def work_days():
    isAdmin = False
    if current_user.profession in ['admin','manager admin','multi admin']:
        flx_s = FlexStatus.query.all()
        isAdmin = True
    else:
        flx_s = FlexStatus.query.filter_by(employee_id=current_user.id).all()
    result_flex = []
    unique_days = set()
    work_time = 0
    for flx in flx_s:
        emp = Employee.query.filter_by(id = flx.employee_id).first()
        unique_days.add(flx.enterTime.date())
        a = flx.exitTime != datetime(1, 1, 1, 1, 1)
        work_time += flx.get_status() if a else 0

        result_flex.append({
            'id': emp.login_id,
            'full_name': f'{emp.name} {emp.surname}',
            'date': str(flx.enterTime.date()),
            'weekDay': ['Mon', 'Tue', 'Wen', 'Thur', 'Fri', 'Sat', 'Sun'][flx.enterTime.weekday()],
            'enter': str(flx.enterTime.time())[:5],
            'out': str(flx.exitTime.time())[:5] if flx.exitTime != datetime(1,1,1,1,1) else '-',
            'duration': f'{flx.get_status() // 3600} hour. {flx.get_status() // 60 % 60} min.' if a else '-',
            'manually': 'yes' if flx.manually else 'no',

        })
    wp = abs(len(unique_days) * 7 * 3600 - work_time)
    context_head = {
        "work_time": f'{work_time // 3600} hour. {work_time // 60 % 60} min.',
        "time_left": f'{wp // 3600} hour. {wp // 60 % 60} min.',
        "number_time_left": len(unique_days) * 7 * 3600 - work_time,
    }

    return render_template('work_day.html', user=current_user,
                           result_flex=result_flex,
                           cntx_head=context_head,
                           isAdmin = isAdmin

                           )


@app.route('/tracking')
def track():
    user_id = current_user.id

    now = datetime.now()
    flex_status = FlexStatus(employee_id=user_id, enterTime=now, exitTime=datetime(1, 1, 1, 1, 1), manually=True)
    db.session.add(flex_status)
    db.session.commit()

    return redirect('home')


@app.route('/mm', methods=['POST', 'GET'])
def nnn():
    if request.method == 'POST':
        a = request.form.get('enterDate')
        b = request.form.get('exitDate')

        def get_dt(date):
            date = str(date)
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:10])
            hour = int(date[11:13])
            minute = int(date[14:16])
            return datetime(year, month, day, hour, minute)

        a = get_dt(a)
        b = get_dt(b)
        flx = FlexStatus(enterTime=a, exitTime=b, employee_id=current_user.id)
        db.session.add(flx)
        db.session.commit()
    return render_template('constant_form.html')
