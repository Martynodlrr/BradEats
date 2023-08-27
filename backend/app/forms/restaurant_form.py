from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, URL
from enum import Enum

restaurant_types=[
    "deals",
    "grocery",
    "convenience",
    "fastFood",
    "alcohol",
    "pharmacy",
    "baby",
    "specialtyFoods",
    "petSupplies",
    "flowers",
    "retail",
    "electronics"
]


class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    image = StringField('Image_Url', validators=[DataRequired(), URL(), Length(max=255)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    category = SelectField('Category',choices=restaurant_types, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    submit = SubmitField('Submit')
