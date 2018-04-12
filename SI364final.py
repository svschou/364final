# SI364 Final Project
# Stephanie Schouman

# Import statements
import os
import json
import datetime
import requests

from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

# Haven't decided if I'll need this yet
from requests_oauthlib import OAuth2Session 
from requests.exceptions import HTTPError

from hp_api_key import hp_api_key

basedir = os.path.abspath(os.path.dirname(__file__))

# App configuration
app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364projectplansvschou"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Login configurations
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


#def make_shell_context():
    #return dict(app=app, db=db, User=User)

# Manager setup
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
#manager.add_command("shell", Shell(make_context=make_shell_context))

## Models

user_students = db.Table('user_students',db.Column('user_id',db.Integer, db.ForeignKey('users.id')),db.Column('student_id',db.Integer, db.ForeignKey('students.id')))

user_spells = db.Table('user_spells',db.Column('user_id',db.Integer, db.ForeignKey('users.id')),db.Column('spell_id',db.Integer, db.ForeignKey('spells.id')))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    hogwarts_house = db.Column(db.String(128))

    students = db.relationship('Student',secondary=user_students,backref=db.backref('users',lazy='dynamic'),lazy='dynamic')
    spells = db.relationship('Spell',secondary=user_spells,backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    house_id = db.Column(db.Integer,db.ForeignKey("houses.id")) # one to many relationship
    patronus = db.Column(db.String(64))
    affilitation = db.Column(db.String(64)) # friend, enemy, study buddy

class Spell(db.Model):
    __tablename__ = "spells"
    id = db.Column(db.Integer, primary_key=True)
    incantation = db.Column(db.String(150))
    spell_type = db.Column(db.String(150))
    description = db.Column(db.String(150))
    # RELATIONSHIP TO USERS



class House(db.Model):
    __tablename__ = "houses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)


## Helper Functions

## View Functions
@app.route('/', methods=["GET","POST"]) # starting page
def index():
    pass 
    # will render_template for base.html, which will include links to all clickable pages and ensures sign in/sign out buttons depending on authentication
    # clickable links include: /sorting_hat, /show_students, /show_spells

@app.route('/login',methods=["GET","POST"])
def login():
    pass
    # allows user to login using a LoginForm

@app.route('/logout')
def logout():
    pass
    # logs out user and redirects user back to /index page

@app.route('/register',methods=["GET","POST"])
def register():
    pass
    # allows user to sign up for an account using registration form, commits changes to users table and redirects user to login page

@app.route('/sorting_hat',methods=["GET","POST"])
def sorting():
    pass
    # has button for user to click to be randomly sorted into a Hogwarts house via a SortingHatForm (just a submit button?), saves returned house to user.hogwarts_house and redirects user to sorting_results.html

@app.route('/sorting_results',methods=["GET","POST"])
def sorting_results():
    pass
    # displays house info for the user

@app.route('/show_students')
def show_students():
    pass
    # queries the students table and displays a list of students that the user has saved
    # there will also be update and delete buttons that will redirect to an update page or redirect back to the show_students (for delete)

@app.route('/show_spells')
def show_spells():
    pass
    # queries the spells table and displays a list of spells that the user has saved 

@app.route('/update_student')
def update_student():
    pass
    # has a update form for the users to change the affiliations between them and the students 

if __name__ == '__main__':
    db.create_all()
    manager.run()
