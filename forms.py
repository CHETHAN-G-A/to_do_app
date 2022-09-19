from flask_wtf.file import FileRequired, FileAllowed ,DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators

## Login Form ##
class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])

## Registration form ##
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

## Todoform ##
class TodoForm(Form):
    title = StringField('Title', [validators.Length(min=6, max=35)])
    description = StringField('Description', [validators.DataRequired()])

## Update Form ##
class UpdateForm(Form):
    title = StringField('Title', [validators.Length(min=6, max=35)])
    description = StringField('Description', [validators.DataRequired()])