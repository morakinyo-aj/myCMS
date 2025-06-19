from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm

class ContentForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description')
    file = FileField('Content File', validators=[
        FileRequired(),
        FileAllowed(['mp4', 'mov', 'jpg', 'jpeg', 'png'], 'Videos and images only!')
    ])
    filepath = StringField('Filepath')
    tags = StringField('Tags (comma separated)')
    submit = SubmitField('Upload')