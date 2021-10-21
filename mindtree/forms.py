from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "id"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "confirm password"})
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
