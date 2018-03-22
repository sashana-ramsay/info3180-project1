from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

class ProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    gender = SelectField(label='Gender', choices=[("Male", "Male"), ("Female", "Female")])
    email = StringField('Email', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    biography = StringField('Biography', widget=TextArea(),validators=[InputRequired()])
    upload = FileField('Pofile Picture',validators=[FileRequired('File required for upload'),FileAllowed(['jpg', 'png'], 'Images only!')])
