from flask_wtf import FlaskForm
from wtforms import SelectField
class StateForm(FlaskForm):
    description: ""
    selections = SelectField("Select a state", choices=[])