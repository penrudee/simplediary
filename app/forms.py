from datetime import datetime
from distutils.text_file import TextFile

from flask_wtf import FlaskForm
from wtforms import TextAreaField,BooleanField,StringField, SelectField ,SubmitField,DecimalField,IntegerField,DateField,RadioField
from wtforms.validators import DataRequired, ValidationError



class LoginForm (FlaskForm):
   username=StringField ('User Name', id='username', validators=[DataRequired()])
   password = StringField('User Password', id='userpassword', validators=[DataRequired()])
   remember_me = BooleanField('Remember Me')
   submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
   username=StringField ('User Name', id='username', validators=[DataRequired()])
   email = StringField('Email', id='Email', validators=[DataRequired()])
   password = StringField('User Password', id='userpassword', validators=[DataRequired()])
   fullname = StringField("Full Name", validators=[DataRequired()])
   contact =  TextAreaField("Address", validators=[DataRequired()])
   nation_id = StringField("Nation Id", validators=[DataRequired()])

class PostForm(FlaskForm):
   head = StringField("Head",render_kw={"placeholder": "Head",'autofocus': True,"tabindex":"1"})
   body = TextAreaField("Body",render_kw={"placeholder": "Type your message here....",'tabindex': "3"})
   tag = StringField("Tag",render_kw={"placeholder": "Tag","tabindex":"4"})
   img_url = StringField("Image Url",render_kw={"placeholder": "Image Url","tabindex":"2"})
   submit = SubmitField("Submit",render_kw={"tabindex":"5"})