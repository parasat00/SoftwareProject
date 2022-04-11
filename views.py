from datetime import datetime
from flask_login import login_required, login_user, logout_user,current_user
from app import app,db
from flask import Flask, flash, redirect,render_template,request
from models import Employee, FlexStatus, load_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
 


@app.route('/profile',methods = ['POST','GET'])
def profile_page():
    user = current_user
    flx = FlexStatus.query.order_by(desc(FlexStatus.enterTime)).filter_by(employee_id = current_user.id).first().get_status()
    print(flx)
    return render_template('profile.html',user = user,flex = flx)



@app.route('/home',methods = ['POST','GET'])
def home():
    user = current_user
    return render_template('dashboard.html',user = current_user)


@app.route('/',methods = ['POST','GET'])
def login_page():
    login_id = request.form.get('id')
    password = request.form.get('password')
    
    if login_id and password:
        user = Employee.query.filter_by(login_id = login_id).first()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
           
            return redirect('/home')
        else:
            flash('Password or login is incorrect ')

    
    return render_template('login.html')

    
@app.route('/hello')
def hello():
    return 'Hello world'        



@app.route('/register',methods = ['POST','GET'])
def register_page():
    if request.method == 'POST':
        login_id = request.form.get('id')
        name = request.form.get('name')
        password = request.form.get('password')
        surname = request.form.get('surname')
        profession = request.form.get('profession')
        
        

        hash_password = generate_password_hash(password)
        emp = Employee(login_id = login_id,name = name,password = hash_password,surname = surname,profession = profession)
        db.session.add(emp)
        db.session.commit()
        login_user(emp)
        
        
        return redirect('/home')
    
        
    return render_template('register.html')


@app.route('/logout',methods = ['POST','GET'])
@login_required
def route_page():
    logout_user()


@app.route('/commands',methods = ['POST','GET'])
def command():
    
    if request.method == 'POST':
        exit = request.form.get('exit')
        enter = request.form.get('enter')

        if enter:
            flx = FlexStatus(employee_id = current_user.id,enterTime = datetime.now())
            print(flx.enterTime)
            db.session.add(flx)
            db.session.commit()
            print('enter',Employee.query.get(flx.employee_id).login_id)
        elif exit:
            flx = FlexStatus.query.order_by(FlexStatus.enterTime).filter_by(employee_id = current_user.id).first()
            flx.exitTime = datetime.now()
            db.session.commit() 
            
            print('exit',Employee.query.get(flx.employee_id).login_id)

    return render_template('qr_commands.html')
    