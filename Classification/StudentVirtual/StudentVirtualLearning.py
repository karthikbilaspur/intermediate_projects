# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import session
from itsdangerous import URLSafeTimedSerializer
import os
import secrets

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_platform.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager(app)

# Initialize Bootstrap
bootstrap = Bootstrap(app)

# Initialize Mail
mail = Mail(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    courses = db.relationship('Course', backref='instructor', lazy=True)

# Define Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship('Tag', backref='course', lazy=True)
    reviews = db.relationship('Review', backref='course', lazy=True)

# Define Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    courses = db.relationship('Course', backref='category', lazy=True)

# Define Tag model
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# Define Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Define course creation form
class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    tags = StringField('Tags')
    submit = SubmitField('Create Course')

# Define review form
class ReviewForm(FlaskForm):
    text = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    return render_template('dashboard.html', courses=courses)

# Course creation route
@app.route('/create-course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        course = Course(title=form.title.data, description=form.description.data, instructor_id=current_user.id, category_id=form.category_id.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_course.html', form=form)

# Review creation route
@app.route('/create-review/<int:course_id>', methods=['GET', 'POST'])
@login_required
def create_review(course_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(text=form.text.data, course_id=course_id, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('course_details', course_id=course_id))
    return render_template('create_review.html', form=form)

# Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form['query']
    courses = Course.query.filter(Course.title.like('%' + query + '%')).all()
    return render_template('search_results.html', courses=courses)

# Pagination route
@app.route('/courses/<int:page>')
def courses(page):
    pagination = Course.query.paginate(page, per_page=10)
    return render_template('courses.html', pagination=pagination)

# Run app
if __name__ == '__main__':
    app.run(debug=True)