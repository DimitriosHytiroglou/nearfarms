from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, PasswordField, validators
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired
#from .model import findUsers, chooseCollection

# # # GENERAL # # #

### General User Login
class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    userType =  SelectField('tripFriend', choices = [('Producer','Producer'),('Consumer','Consumer')])



# # # Consumers # # #

### Add New Consumer
class NewConsumerForm(Form):
    first_name = StringField('firstName', validators=[DataRequired()])
    last_name = StringField('lastName', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])




# # # PRODUCERS # # #

### Add New Producer
class NewProducerForm(Form):
    first_name = StringField('firstName', validators=[DataRequired()])      # John
    last_name = StringField('lastName', validators=[DataRequired()])        # Farmer
    farm_name = StringField('farmName', validators=[DataRequired()])    	# John Farmer Farms LLC
    email = EmailField('email', validators=[DataRequired()])                # john.farmer@gmail.com
    username = StringField('username', validators=[DataRequired()])         # j_farmer
    password = PasswordField('password', validators=[DataRequired()])       # pAsSwOrD
    
    # Is this the WTF form type to be used for free text? 
    # Also, this should be optional initially.
    farm_description = StringField('description')


###ADD NEW PRODUCT FORM
class ProductForm(Form):
    product = StringField('product', validators=[DataRequired()])
    productType = StringField('productType', validators=[DataRequired()])
    subType = StringField('subType', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])			 # probably need to change this to float
    image = StringField('image', validators=[DataRequired()]) 			 # this is just a placeholder for now




# # # MARKETS # # #

class NewMarketForm(Form):
    
    # Define rules of uniquness for this.
    market_name = StringField('producerName', validators=[DataRequired()])   # Monterey Market

    # This needs to be something that gives a good Google Maps point. 
    # Could we be adding it throught Google Maps to ensure that? Instead of typing out an address.
    location = StringField('producerName', validators=[DataRequired()])      # Monterey Market

    # Is this the WTF form type to be used for free text? 
    # Also, this should be optional initially.
    description = StringField('description')

    # Do markets need accounts? and credentials? Who handles them?
    email = EmailField('email', validators=[DataRequired()])                 # Monterey Market Email
    
    # Should this be called maybe MarketID or something?
    username = StringField('username', validators=[DataRequired()])          # mont_markt
    password = PasswordField('password', validators=[DataRequired()])        # pAsSwOrD

    # What else to be added?

