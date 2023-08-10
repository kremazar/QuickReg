from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,SelectField,DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_wtf.file import FileAllowed, FileRequired
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    picture = TextAreaField('Base64 Encoded Image', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')
        
class RegistrationForm2(FlaskForm):
    """ name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    citizenship = StringField('Citizenship', validators=[DataRequired()]) """
    picture = TextAreaField('Base64 Encoded Image', validators=[DataRequired()])
    submit = SubmitField('Register')

        

class RecognitionForm(FlaskForm):
    picture = TextAreaField('Base64 Encoded Image', validators=[DataRequired()])
    submit = SubmitField('Register')

class UploadDocumentForm(FlaskForm):
    front_document = FileField('Front Document', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    back_document = FileField('Back Document', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload')

class ProfileForm(FlaskForm):
    surname = StringField('Surname')
    name = StringField('Name')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    country = StringField('Country')
    residence = StringField('Residence')
    oib = StringField('OIB')
    submit = SubmitField('Save Changes')    

class ProfileForm2(FlaskForm):
    surname = StringField('Surname')
    name = StringField('Name')
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')])
    country = StringField('Country')
    citizenship = StringField('Citizenship')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    identity_card_number = StringField('Identity Card Number')
    date_of_expiry = DateField('Date of Expiry')
    residence = StringField('Residence')
    date_of_issue = DateField('Date of Issue')
    oib = StringField('OIB')
    submit = SubmitField('Save Changes') 