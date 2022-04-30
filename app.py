from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

DEBUG = True
app = Flask(__name__)
app.secret_key = 'multi secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)

from views import *
from models import *

if __name__ == '__main__':
    app.run(debug=DEBUG)
