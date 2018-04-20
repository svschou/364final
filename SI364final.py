# SI364 Final Project
# Stephanie Schouman

# Import statements
import os
import json
import datetime
import requests
from bs4 import BeautifulSoup

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
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364finaltest"
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

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None


## MODELS

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
    affil = db.Column(db.String(64)) # friend, enemy, study buddy
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User",backref='Student')

class Spell(db.Model):
    __tablename__ = "spells"
    id = db.Column(db.Integer, primary_key=True)
    incantation = db.Column(db.String(150))
    spell_type = db.Column(db.String(150))
    description = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # RELATIONSHIP TO USERS
    user = db.relationship("User",backref='Spell')


class House(db.Model):
    __tablename__ = "houses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)


## HELPER FUNCTIONS

# FROM PROJECT PLAN
def get_char_data(char_name):
    base_url = "https://www.potterapi.com/v1/"
    hp_api_key = "$2a$10$XPnZrHnIYgf.R9etCbM/8eHqwCnygF9MlSVbcVA4wDlPsIZpwsZa2"

    params = {"key":hp_api_key,"name": char_name}

    response = requests.get(base_url+"characters",params=params)
    hp_list = json.loads(response.text)

    student_name = hp_list[0]["name"]
    #student_house = form_house
    student_house = hp_list[0]["house"]
    if "patronus" in hp_list[0]:
        student_patronus = hp_list[0]["patronus"]
    else:
        student_patronus = "No known patronus" 

    return (student_name,student_house,student_patronus) # tup

def get_sorting_house():
	base_url = "https://www.potterapi.com/v1/"

	response = requests.get(base_url+"sortingHat")
	hp_house = json.loads(repsonse.text)
	return hp_house



def get_spells_info():
	results = requests.get('https://www.pojo.com/harry-potter-spell-list/')
	soup = BeautifulSoup(results.text, 'html.parser')

	table_soup = soup.find('table')
	#print(table_soup)
	rows_soup = table_soup.find_all('tr')
	#print(rows_soup[2])

	list_of_spells_tup = []

	for row in rows_soup[2:]:
		spell_soup = row.find_all('td')
		# empty rows in the table, checking there is actual data
		if len(spell_soup[0].text) > 1:
			#print(spell_soup[0].text)
			spell_incantation = spell_soup[0].text
			spell_type = spell_soup[1].text
			spell_description = spell_soup[2].text
			#print(spell_incantation,spell_type, spell_description)
			list_of_spells_tup.append((spell_incantation,spell_type, spell_description))
	return list_of_spells_tup

list_of_spells = get_spells_info()

def get_or_create_house(db_session, house_name):
    house = db_session.query(House).filter_by(name=house_name).first()
    if house:
        return house
    else:
        house = House(name=house_name)
        db_session.add(house)
        db_session.commit()
        return house

def get_or_create_student(db_session, st_name, st_house, st_patronus, st_affil,current_user):
    student = db_session.query(Student).filter_by(name=st_name,user_id=current_user.id).first()
    if student:
        return student
    else:
        house = get_or_create_house(db_session, st_house)
        student = Student(name=st_name,house_id=house.id,patronus=st_patronus,affil=st_affil,user_id=current_user.id)
        db_session.add(student)
        db_session.commit()

        current_user.students.append(student)
        db_session.add(current_user)
        db_session.commit()
        return student

def get_or_create_spell(db_session, spell_tup, current_user):
	spell = db_session.query(Spell).filter_by(incantation=spell_tup[0],user_id=current_user.id).first()
	if spell:
		return spell
	else:
		spell = Spell(incantation=spell_tup[0],spell_type=spell_tup[1],description=spell_tup[2],user_id=current_user.id)
		db_session.add(spell)
		db_session.commit()

		current_user.spells.append(spell)
		db_session.add(current_user)
		db_session.commit()

		return spell

## FORMS
# GIPHY HOMEWORK - PROVIDED
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# SIMILAR TO MIDTERM
# CHANGES: not requiring house, requiring affiliation
class SearchStudentForm(FlaskForm):
    name = StringField("Search for a Hogwarts Student to befriend or duel: ",validators=[Required()])
    def validate_name(form,field):
        if " " not in field.data:
            raise ValidationError("Please enter the first and last name separated by a space")
    affil = StringField("Enter your affiliation with this student (friend, enemy, etc.): ",validators=[Required()])
    submit = SubmitField('Search Hogwarts Students')

class SearchSpellForm(FlaskForm):
	spell = StringField("Enter the name of a spell or charm you'd like to learn: ",validators=[Required()])
	def validate_spell(form,field):
		for char in field.data:
			if char in "1234567890":
				raise ValidationError("Please enter a spell name without any numbers in it")
	submit = SubmitField('Search Spells')

## UPDATE FORMS
class UpdateAffilButtonForm(FlaskForm):
	submit = SubmitField("Update Affiliation")

class UpdateAffilForm(FlaskForm):
	new_affil = StringField("Update your affiliation with this Hogwarts student: ",validators=[Required()])
	submit = SubmitField("Update")

class DeleteStudentForm(FlaskForm):
	submit = SubmitField("Delete this Student")

class DeleteSpellForm(FlaskForm):
	submit = SubmitField("Delete this Spell")

## View Functions
@app.route('/', methods=["GET","POST"]) # starting page
@login_required
def index():
    student_form = SearchStudentForm()
    spell_form = SearchSpellForm()
    if student_form.validate_on_submit(): 
        print("formed submitted")
        student_data = get_char_data(student_form.name.data) # tup name, house, patronus
        print(student_data)
        student = get_or_create_student(db.session, st_name=student_data[0],st_house=student_data[1],st_patronus=student_data[2],st_affil=student_form.affil.data,current_user=current_user)
        print(student)
        return redirect(url_for("show_students"))

    if spell_form.validate_on_submit():
        spell_name = spell_form.spell.data
        for tup in list_of_spells:
            if tup[0].lower() == spell_name.lower():
                spell = get_or_create_spell(db.session,tup,current_user)
                print(spell)
                return redirect(url_for("show_spells"))

    # will render_template for base.html, which will include links to all clickable pages and ensures sign in/sign out buttons depending on authentication
    # clickable links include: /sorting_hat, /show_students, /show_spells
    print("form didn't submit?")
    return render_template("index.html",form=student_form,form2=spell_form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)
    # allows user to login using a LoginForm

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))
    # logs out user and redirects user back to /index page

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)
    # allows user to sign up for an account using registration form, commits changes to users table and redirects user to login page

@app.route('/sorting_hat',methods=["GET","POST"])
def sorting():
    pass
    # has button for user to click to be randomly sorted into a Hogwarts house via a SortingHatForm (just a submit button?), saves returned house to user.hogwarts_house and redirects user to sorting_results.html

@app.route('/sorting_results',methods=["GET","POST"])
def sorting_results():
    pass
    # displays house info for the user

@app.route('/show_students',methods=["GET","POST"])
#@login_required
def show_students():
    update_form = UpdateAffilButtonForm()
    delete_form = DeleteStudentForm()
    # queries the students table and displays a list of students that the user has saved
    # there will also be update and delete buttons that will redirect to an update page or redirect back to the show_students (for delete)
    student_list = Student.query.filter_by(user_id=current_user.id).all()
    student_tups = []
    for st in student_list:
        house = house = House.query.filter_by(id=st.house_id).first()
        student_tups.append((st,house))
    return render_template("show_students.html",lst=student_tups,form_up=update_form,form_del=delete_form)

@app.route('/show_spells')
#@login_required
def show_spells():
    # queries the spells table and displays a list of spells that the user has saved 
    delete_form = DeleteSpellForm()
    spell_list = Spell.query.filter_by(user_id=current_user.id).all()
    return render_template("show_spells.html",lst=spell_list,form=delete_form)

@app.route('/update_student/<student>',methods=["GET","POST"])
def update_student(student):
	form = UpdateAffilForm()
	s = Student.query.filter_by(id=student).first()
	print(s.name)
	if form.validate_on_submit():
		print("inside if statement")
		new_affil = form.new_affil.data
		s = Student.query.filter_by(id=student).first()
		s.affil = new_affil
		db.session.commit()

		flash("Successfully updated {}'s affiliation!".format(s.name))
		return redirect(url_for("show_students"))
	print("form not validated")
	return render_template("update_student.html",student=s,form=form)
    # has a update form for the users to change the affiliations between them and the students 

@app.route('/delete_student/<student>',methods=["GET","POST"])
def delete_student(student):
	s = Student.query.filter_by(id=student).first()
	db.session.delete(s)
	db.session.commit()

	flash("Successfully deleted {} from your list of students.".format(s.name))
	return redirect(url_for("show_students"))

@app.route('/delete_spell/<spell>',methods=["GET","POST"])
def delete_spell(spell):
	sp = Spell.query.filter_by(id=spell).first()
	db.session.delete(sp)
	db.session.commit()

	flash("Successfully deleted {} from your list of spells.".format(sp.incantation))
	return redirect(url_for("show_spells"))

if __name__ == '__main__':
    db.create_all()
    manager.run()
    app.run(use_reloader=True, debug=True)
