from flask_wtf import FlaskForm
from wtforms import StringField,widgets,SelectField,SubmitField
from wtforms.validators import DataRequired

choices = ["bike_dangerous", "walk_dangerous","drive_dangerous","bike_safe","walk_safe","drive_safe"]
weight = ["fast","safe"]

class Location(FlaskForm):
    location_start = StringField(label= "From",validators=[DataRequired()])
    location_to = StringField(label = "To",validators=[DataRequired()])
    transportation = SelectField(u"Transportation",choices=choices)
    pick = SelectField(u"Transportation",choices=weight)
    submit = SubmitField("Navigate !")
