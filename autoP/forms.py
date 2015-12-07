from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, StopValidation, ValidationError

from autoP.models import User


class LoginForm(Form):
    def generate_csrf_token(self, csrf_context):
        pass

    email = StringField('Email', validators={DataRequired(), Length(1, 64), Email()})
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')





class RegistrationForm(Form):
    email = StringField('Email', validators={DataRequired(), Length(1, 64), Email()})

    # def validate_email(form, field):
    #     from autoP.models import User
    #     if User.get_by(email=field.data):
    #         raise StopValidation('Email already registered.')

    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    submit = SubmitField('Register')

    def generate_csrf_token(self, csrf_context):
        pass




class SearchForm(Form):
    def generate_csrf_token(self, csrf_context):
        pass
    search = StringField('', validators={DataRequired(), Length(1, 128)})
    # submit = SubmitField('Find')
