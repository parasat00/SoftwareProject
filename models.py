from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime


class Card(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f'<Card %r>' % self.id


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    login_id = db.Column(db.String(10), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    flex_status = db.relationship('FlexStatus', backref='flex_status')
    # assigned_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    # assignedUser = db.relationship('Employees',backref = 'employee')


    def __repr__(self) -> str:
        return "<Employee %r> " % self.id


class FlexStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    name = db.Column(db.String)
    issue = db.Column(db.String(100),default='')
    enterTime = db.Column(db.DateTime(), nullable=True)
    exitTime = db.Column(db.DateTime())
    manually = db.Column(db.Boolean(), default=False,nullable=True)

    def get_status(self):
        tmp = self.exitTime - self.enterTime
        return tmp.seconds

    def get_date(self):
        return self.enterTime.date()

    def __repr__(self) -> str:
        return f'<FlexStatus %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)
