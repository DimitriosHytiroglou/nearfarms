import os
from flask import session, render_template, redirect, request, flash
from app import app, models
from .forms import *
from .models import *
from werkzeug import secure_filename
from app.encryption.HashingHandler import *
import json
# Access the models file to use SQL functions

@app.route('/')
def index():

    session['username'] = None
    session['password'] = None

    session['user_type'] = None

    user_status = {}
    user_status['in'] = 'block'
    user_status['out'] = 'none'

    session['status'] = user_status

    return redirect('/home')
    #return redirect('/farmer_home')

@app.route('/home', methods=['GET'])
def home():
    
    return render_template('home.html', user=session['username'], user_status=session['status'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)

    session['status']['in'] = 'block'
    session['status']['out'] = 'none'

    session.pop('user_type', None)

    return redirect('/')

# App routing for USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    
    wrong = 'none'

    if loginForm.validate_on_submit():
        
        u = loginForm.username.data
        p = loginForm.password.data
        t = loginForm.userType.data.lower()

        collection = chooseCollection('users')
        userPass = getUserPass(collection, u)

        #  NEED TO ADD A CHECK HERE THAT USERS CHOOSE APPROPRIATELY WHAT THEY ARE SO THEY ARE NOT LOGGED IN BUT WITHOUT ACCESS
        print("t=",t)
        if userPass != []:
            if checkPass(userPass,p) and getUserType(collection,u)==t:
                session['username'] = u
                session['password'] = userPass

                session['status']['in'] = 'none'
                session['status']['out'] = 'block'


                if t == 'producer':
                    session['user_type'] = 'producer'
                    return redirect('/farmer_home')

                elif t == 'consumer':
                    session['user_type'] = 'consumer'
                    return redirect('/shop_produce')
            else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong, user=session['username'], user_status=session['status'])
        else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong, user=session['username'], user_status=session['status'])

    return render_template('login.html', loginForm=loginForm, wrong=wrong, user=session['username'], user_status=session['status'])




# App routing to CREATE FARMER ACCOUNT
@app.route('/create_newProducer', methods=['GET', 'POST'])
def create_newProducer():
    
    wrong = 'none'

    newProducerForm = NewProducerForm()
    if newProducerForm.validate_on_submit():
        first_name = newProducerForm.first_name.data
        last_name = newProducerForm.last_name.data
        farm_name = newProducerForm.farm_name.data
        email = newProducerForm.email.data
        username = newProducerForm.username.data
        password = newProducerForm.password.data
        farm_description = newProducerForm.farm_description.data
        user_type = 'producer'

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertProducer(collection, email, username, password, first_name, last_name, farm_name, farm_description, user_type)

            session['username'] = username
            session['password'] = password

            session['status']['in'] = 'none'
            session['status']['out'] = 'block'

            session['user_type'] = 'producer'

            # Create directory to save images of this producer
            if not os.path.exists('file_uploads/'+username):
                os.makedirs('file_uploads/'+username)

            return redirect('/farmer_home') 


        else:
            wrong = 'block'
            return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong, user=session['username'], user_status=session['status'])

    return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong, user=session['username'], user_status=session['status'])


# App routing to CREATE USER
@app.route('/create_newConsumer', methods=['GET', 'POST'])
def create_newConsumer():
    
    wrong = 'none'

    newConsumerForm = NewConsumerForm()
    if newConsumerForm.validate_on_submit():
        first_name = newConsumerForm.first_name.data
        last_name = newConsumerForm.last_name.data
        email = newConsumerForm.email.data
        username = newConsumerForm.username.data
        password = newConsumerForm.password.data
        user_type = 'consumer'

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertConsumer(collection, email, username, password, first_name, last_name, user_type)

            session['username'] = username
            session['password'] = password

            session['status']['in'] = 'none'
            session['status']['out'] = 'block'

            session['user_type'] = 'consumer'

            return redirect('/shop_produce')

        else:
            wrong = 'block'
            return render_template('register_consumer.html', newConsumerForm=newConsumerForm, wrong=wrong, user=session['username'], user_status=session['status'])

    return render_template('register_consumer.html', newConsumerForm=newConsumerForm, wrong=wrong, user=session['username'], user_status=session['status'])



# App routing to ADD PRODUCE
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    productForm = ProductForm()
    if productForm.validate_on_submit():
        # Get data from the form
        # Send data from form to Database
        producerID = session['username']
        product = productForm.product.data
        productType = productForm.productType.data
        subType = productForm.subType.data
        quantity = productForm.quantity.data
        price = productForm.price.data
        image = ''
        # image = productForm.image.data

        collection = chooseCollection('products')
        insert_products(collection, producerID, product, productType, subType, quantity, price, image)

        return redirect('/farmer_home')
    return render_template('product.html', productForm=productForm, user=session['username'], user_status=session['status'])

@app.route('/farmer_home', methods=['GET'])
def farmer_home():
    # Retreive data from database to display
    if session['username'] != None and session['user_type']=='producer':
        
        collection = chooseCollection('products')
    
        products = retrieve_products(collection,session['username'])
    
        productList = []
    
        for product in products:
            productList.append(product)
    
        return render_template('farmer.html', productList=productList, user=session['username'], user_status=session['status'])

    else:
        flash('You were successfully logged in')
        return redirect('/home')

@app.route('/product_update', methods=['POST'])
def productUpdate():
    
    # Retrieve data from database to display
    collection = chooseCollection('products')
    
    if request.method == "POST":
       

        update_product(collection, request.form['_id'], request.form['product'], request.form['productType'], request.form['subType'], request.form['quantity'], request.form['price'])     

        products = retrieve_products(collection,session['username'])

        productList = []

        for product in products:
            productList.append(product)
     
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



@app.route('/product_delete', methods=['POST'])
def productDelete():
    
    # Retrieve data from database to display
    collection = chooseCollection('products')
    
    if request.method == "POST":
       
        products = retrieve_products(collection,session['username'])

        productList = []

        for product in products:
            productList.append(product)
     
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/consumer_home', methods=['GET'])
def consumer_home():
    
    pass

    #UNCOMMENT when template is created
    # return render_template('consumer.html')

@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():

    UPLOAD_FOLDER = 'app/static/file_uploads/'+session['username']+'/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### NEED TO FIX ALL THE RETURN FIELDS IN THE FOLLOWING CODE

### NEED TO ADD CHECK FOR IF FILE EXISTS WITH SAME NAME TO NOT OVEWRITE
### ACTUALLY, NEED TO RENAME FILE UPON SAVING WITH RANDOM CODE AND SAVE THAT IN DATABASE

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/farmer_home')
        file = request.files['file']
        
        from werkzeug.datastructures import ImmutableMultiDict
        data = dict(request.form)


        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/farmer_home')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            collection = chooseCollection('products')
            image = 'file_uploads/'+session['username']+'/'+filename
            update_image(collection, data['_id'][0], image)

            flash('File uploaded succesfully!')
            return redirect('/farmer_home')


@app.route('/shop_produce', methods=['POST','GET'])
def shop_produce():

    collection = chooseCollection('products')

    
    all_produce = retrieve_all_produce(collection)
    
    # gathering all of the produce listed in database
    produceList = []

    # gathing all of the products, productypes, subtypes, 
    ProductList = []
    ProductTypeList = []
    SubTypeList = []

    for produce in all_produce:
        produceList.append(produce)
        ProductList.append(produce['Product'])
        ProductTypeList.append(produce['Product Type'])
        SubTypeList.append(produce['Sub Type'])

    # getting unique values and sorting in alphabetical order
    ProductList = sorted(list(set(ProductList)))
    ProductTypeList = sorted(list(set(ProductTypeList)))
    SubTypeList = sorted(list(set(SubTypeList)))
    
    filters = {}
    filters['product'] = ''
    filters['productType'] = ''
    filters['subType'] = ''

    return render_template('shop_produce.html', produceList=produceList, ProductList=ProductList, ProductTypeList= ProductTypeList,\
        SubTypeList=SubTypeList, filters=filters, user=session['username'], user_status=session['status'])

@app.route('/apply-filter', methods=['POST'])
def applyFilter():
    
    filters = {}

    if request.method == "POST":

        filters['product'] = request.form['product']
        filters['productType'] = request.form['productType']
        filters['subType'] = request.form['subType']


    ###########################################################
    #  GET THE PRODUCE, SAME AS ABOVE, THIS MUST BE SIMPLIFIED
    ###########################################################

    collection = chooseCollection('products')

    all_produce = retrieve_all_produce(collection)
    
    # gathering all of the produce listed in database
    produceList = []

    # gathing all of the products, productypes, subtypes, 
    ProductList = []
    ProductTypeList = []
    SubTypeList = []

    for produce in all_produce:
        if (filters['product'] == '' and filters['productType'] == '' and filters['subType'] == ''):
            produceList.append(produce)
        elif (filters['product'] == produce['Product'] or filters['productType'] == produce['Product Type'] or filters['subType'] == produce['Sub Type']):
            produceList.append(produce)
        
        ProductList.append(produce['Product'])
        ProductTypeList.append(produce['Product Type'])
        SubTypeList.append(produce['Sub Type'])

    # getting unique values and sorting in alphabetical order
    ProductList = sorted(list(set(ProductList)))
    ProductTypeList = sorted(list(set(ProductTypeList)))
    SubTypeList = sorted(list(set(SubTypeList)))
    
    ##########################################
    # APPLYING THE FILTERS
    ##########################################

        
    # return redirect('/farmer_home', filters=filters)
    return render_template('shop_produce.html', produceList=produceList, ProductList=ProductList, ProductTypeList= ProductTypeList,\
        SubTypeList=SubTypeList, filters=filters, user=session['username'], user_status=session['status'])

    


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html', user=session['username'], user_status=session['status']), 404