from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class UsernameForm(FlaskForm):

    username = StringField('Reddit Username', validators=[DataRequired()])
    with_download = BooleanField('download a local copy ')
    with_archive = BooleanField('backup to archive.is')
    submit = SubmitField("Get Data!")
