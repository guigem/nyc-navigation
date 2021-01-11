from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FloatField,widgets,SelectField
from wtforms.validators import DataRequired

choices = ["bike_dangerous", "walk_dangerous","drive_dangerous","bike_safe","walk_safe","drive_safe"]

class Location(FlaskForm):
    location = StringField("Location")
    starting_point_long = FloatField("From (long)")
    starting_point_lat =  FloatField("From (lat)")
    dest_point_long = FloatField("To (long)")
    dest_point_lat = FloatField("To (lat)")
    transportation = SelectField(u'Programming Language', choices=choices)
    submit = SubmitField("Navigate")
