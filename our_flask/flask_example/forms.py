from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

class SubmitForm(FlaskForm):
    spread_sheet_url = StringField('Please insert your Google SpreadSheet url', validators=[DataRequired(), Regexp("https?://.*")])
    submit = SubmitField('Submit')



