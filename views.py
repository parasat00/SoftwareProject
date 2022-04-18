from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from flask import Flask, flash, redirect, render_template, request
from models import Employee, FlexStatus, load_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc


@app.route('/profile', methods=['POST', 'GET'])
def profile_page():
    user = current_user
    flx = FlexStatus.query.order_by(desc(FlexStatus.enterTime)).filter_by(
        employee_id=current_user.id).first().get_status()
    print(flx)
    return render_template('profile.html', user=user, flex=flx)


@app.route('/home', methods=['POST', 'GET'])
def home():
    user = current_user
    week_day = datetime.now().weekday()
    now = {
        'today_date':datetime.now(),
        'week_day':['Mon','Tue','Wen','Thur','Fri','Sat','Sun'][week_day]
    }
    # today week chek

    dates_status = FlexStatus.query.filter_by(employee_id = current_user.id).all()
    # current_week_days = []
    def week_activity():
        f = week_day - week_day % 7
        l = week_day + (7 - week_day % 7)
        work_time = 0
        for status in dates_status:

            if f <= status.enterTime.weekday()<= l:
                work_time += status.get_status() // 60

        activity = f'{(work_time / 2700)*100:.2f}%'
        return activity,work_time,(2700 - work_time)

    wa,wt,hr = week_activity()
    hr = f'{hr//60}:{hr//60%60}'
    worked_activity = {
        'weekly_activity':wa,
        'worked_time':wt,
        'hours_remained':hr,
    }

    print(worked_activity)

    return render_template('dashboard.html',
                           user = current_user,
                           now = now,
                           worked_activity = worked_activity


                           )


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


@app.route('/hello')
def hello():
    return 'Hello world'


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
def route_page():
    logout_user()


@app.route('/mm',methods = ['POST','GET'])
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
            return datetime(year,month,day,hour,minute)
        a = get_dt(a)
        b = get_dt(b)
        flx = FlexStatus(enterTime = a,exitTime = b,employee_id = current_user.id)
        db.session.add(flx)
        db.session.commit()
    return render_template('constant_form.html')