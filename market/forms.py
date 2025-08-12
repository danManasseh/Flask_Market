from tokenize import String
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired
from .models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        

    def validate_email_address(self, email_adddress_to_check):
        email = User.query.filter_by(email_address = email_adddress_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email address')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class UpdateItemForm(FlaskForm):
    name = StringField(label='Name of Item:', validators=[Length(min=2, max=30), DataRequired()])
    price = IntegerField(label='Price of Item:', validators=[DataRequired()])
    barcode = StringField(label='Item Barcode:', validators=[Length(min=12, max=12), DataRequired()])
    description = TextAreaField(label='Item Description:', validators=[Length(max=1024)])
    submit = SubmitField(label='Update Item')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')