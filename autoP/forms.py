from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(Form):
    email = StringField('Email', validators={DataRequired(), Length(1, 64), Email()})
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email=StringField('Email', validators=[DataRequired, Length(1, 64), Email])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        from autoP.User import User
        if User.get_by(email=field.data).first():
            raise ValidationError('Email already registered.')
