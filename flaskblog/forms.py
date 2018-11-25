from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Enter Your Username: ',
                            validators =[DataRequired(), Length(min=2,max=20)])

    email = StringField('Enter Your Email Address: ',
                        validators = [DataRequired() ,Email()])

    password = PasswordField('Enter Your Password: ', validators = [DataRequired()])

    confirm_password = PasswordField('Confirm Your Password: ',
                                    validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')


    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exists. Please enter a different one.')


class LoginForm(FlaskForm):
    email = StringField('Enter Your Email Address: ',
                        validators = [DataRequired() ,Email()])

    password = PasswordField('Enter Your Password: ', validators = [DataRequired()])

    remember = BooleanField('Remember Me?')

    submit = SubmitField('Login')


################################################################################


class UpdateAccountForm(FlaskForm):
    username = StringField('Username: ',
                            validators =[DataRequired(), Length(min=2,max=20)])

    email = StringField('Email Address: ',
                        validators = [DataRequired() ,Email()])

    picture = FileField('Update Profile Picture:', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update Profile')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')


    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exists. Please enter a different one.')
