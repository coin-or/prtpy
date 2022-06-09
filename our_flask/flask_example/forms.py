from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, URL


class SubmitForm(FlaskForm):
    link = URL()
    spread_sheet_url = StringField('Copy here the input file link : \n '
                                   , validators=[DataRequired(), Regexp("https?://.*")])
    submit = SubmitField('Submit')



