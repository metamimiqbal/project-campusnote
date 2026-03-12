from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import Email, Length, DataRequired, EqualTo, ValidationError
from campusnote import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
    submit = SubmitField('Register', validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        
        if user:
            raise ValidationError('This username is already taken. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data)
        
        if user:
            raise ValidationError('This email is already registered. Please log in instead.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login', validators=[DataRequired()])

    # checking in database whether password match or not - later
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update', validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        
        if user:
            raise ValidationError('This username is already taken. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data)
        
        if user:
            raise ValidationError('This email is already registered. Please log in instead.')