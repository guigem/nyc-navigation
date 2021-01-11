from flask_wtf import FlaskForm
from wtforms import StringField,widgets,SelectField,SubmitField
from wtforms.validators import DataRequired

choices = ["bike","walk","drive"]
weight = ["fast","safe","do you want to die?"]

class Location(FlaskForm):
    location_start = StringField(label= "Point de départ",validators=[DataRequired()])
    location_to = StringField(label = "Destination",validators=[DataRequired()])
    transportation = SelectField(u"Transportation",choices=choices)
    pick = SelectField(u"Transportation",choices=weight)
    submit = SubmitField("Navigate !")
