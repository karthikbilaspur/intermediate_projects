# project/forms/registration_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    """
    Registration form class.

    Attributes:
        username (StringField): Username field.
        password (PasswordField): Password field.
        confirm_password (PasswordField): Confirm password field.
        submit (SubmitField): Submit button.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=80)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")