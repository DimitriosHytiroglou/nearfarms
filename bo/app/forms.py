from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired

class ProductForm(Form):
    product = StringField('product', validators=[DataRequired()])
    productType = StringField('productType', validators=[DataRequired()])
    subType = StringField('subType', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()]) # probably need to change this to float
    image = StringField('image', validators=[DataRequired()]) # this is just a placeholder for now

