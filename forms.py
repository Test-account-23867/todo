from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email=EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit=SubmitField('Submit')


class RegisterForm(FlaskForm):
    name=StringField('Name: ')
    email=EmailField('Email: ')
    password=PasswordField('Password: ')
    submit=SubmitField('Submit ')


class ItemForm(FlaskForm):
    item = StringField('Item: ')
    submit = SubmitField('➕')