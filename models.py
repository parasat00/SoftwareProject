from flask_login import UserMixin
from main import db,login_manager

class Employee(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    login_id = db.Column(db.String(9),unique = True,nullable = False)
    name = db.Column(db.String(100),nullable = False)
    surname = db.Column(db.String(100),nullable = False)
    profession = db.Column(db.String(30),nullable = False)
    password = db.Column(db.String(40),nullable  = False)


    def __repr__(self) -> str:
        return "<Employee %r> " % self.id

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)