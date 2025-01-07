# project/forms/login_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    Login form class.

    Attributes:
        username (StringField): Username field.
        password (PasswordField): Password field.
        submit (SubmitField): Submit button.
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")