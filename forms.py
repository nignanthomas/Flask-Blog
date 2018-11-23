from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Enter Your Username: ',
                            validators =[DataRequired(), Length(min=2,max=20)])

    email = StringField('Enter Your Email Address: ',
                        validators = [DataRequired() ,Email()])

    password = PasswordField('Enter Your Password: ', validators = [DataRequired()])

    confirm_password = PasswordField('Confirm Your Password: ',
                                    validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
