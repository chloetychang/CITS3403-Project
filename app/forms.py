# Define forms using Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select...'), ('male', 'Male'), ('female', 'Female'), ('prefer_not_to_say', 'Prefer not to say')], validators=[DataRequired(message="Please select a gender.")])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    # # Password validation , requires a minimum of 6 characters and must match the confirm password field
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')