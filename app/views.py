import os
from flask import session, render_template, redirect, request, flash
from app import app, models
from .forms import *
from .models import *
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
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
    
    return render_template('homepage.html', user=session['username'], user_status=session['status'])

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
        
        # Gets hashed password associated with this username
        userPass = getUserPass(collection, u)
        
        if userPass != []:
            if checkPass(userPass,p) and getUserType(collection,u)==t:
                session['username'] = u
                session['password'] = userPass

        # Sets the session variable for the Login/Logout button
                session['status']['in'] = 'none'
                session['status']['out'] = 'block'

        # Checks the type of user loggin in and sets the session['user_type'] variable
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
        image = ''

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertProducer(collection, email, username, password, first_name, last_name, farm_name, farm_description, user_type, image)

            session['username'] = username
            session['password'] = password

            session['status']['in'] = 'none'
            session['status']['out'] = 'block'

            session['user_type'] = 'producer'

            # Create directory to save images of this producer
            if not os.path.exists('app/static/file_uploads/'+username):
                os.makedirs('app/static/file_uploads/'+username)

            return redirect('/farmer_home') 

        else:
            wrong = 'block'
            return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong, user=session['username'], user_status=session['status'])

    return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong, user=session['username'], user_status=session['status'])


# App routing to CREATE USER
@app.route('/create_newConsumer', methods=['GET', 'POST'])
def create_newConsumer():
    
# Set variable that determines "Wrong username or password" message
    wrong = 'none'

    newConsumerForm = NewConsumerForm()
    
    if newConsumerForm.validate_on_submit():
        
    # Retrieve user inserted values from from
        first_name = newConsumerForm.first_name.data
        last_name = newConsumerForm.last_name.data
        email = newConsumerForm.email.data
        username = newConsumerForm.username.data
        password = newConsumerForm.password.data
        user_type = 'consumer'

    # Check if username exists in database
        collection = chooseCollection('users')
        
        userPass = getUserPass(collection, username)
        
        if userPass == []:
        # Hash password to be saved in database
            password = hashPass(password)

        # Insert new consumer user in the database
            collection = chooseCollection('users')
            insertConsumer(collection, email, username, password, first_name, last_name, user_type)

        # Set username and password session variables
            session['username'] = username
            session['password'] = password

        # Set session variable that determines Login/Logout button
            session['status']['in'] = 'none'
            session['status']['out'] = 'block'

        # Set session variable that determines user access to features
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
        marketID = productForm.marketID.data
        product = productForm.product.data
        productType = productForm.productType.data
        units = productForm.units.data
        quantity = productForm.quantity.data
        price = str(round(productForm.price.data,2)) # have to convert to string since mongodb doesn't take decimals
        image = ''
        # image = productForm.image.data

        collection = chooseCollection('products')
        insert_products(collection, producerID, product, productType, units, quantity, price, image, marketID)

        return redirect('/farmer_home')
    return render_template('product.html', productForm=productForm, user=session['username'], user_status=session['status'])


@app.route('/farmer_home', methods=['GET'])
def farmer_home():
    # Retreive data from database to display
    if session['username'] != None and session['user_type']=='producer':
        
        collection = chooseCollection('products')
    
        products = retrieve_products(collection,session['username'])
    
        productList = []
        marketList = []
        
        for product in products:
            productList.append(product)
            marketList.append(product['MarketID'])
        
        marketList = sorted(list(set(marketList)))
        
    # Get Farmer data
        collection = chooseCollection('users')
        farmerDeets = getFarmData(collection, session['username'])
        farmerList = []
        [farmerList.append(deets) for deets in farmerDeets]    
        farmer = farmerList[0]

        # blank filter
        filters = {'MarketID':''}
        
        return render_template('farmer.html', marketList=marketList, filters=filters, productList=productList, farmer = farmer, user=session['username'], user_status=session['status'])

    else:
        flash('You were successfully logged in')
        return redirect('/home')


@app.route('/apply-filter-farmer', methods=['POST'])
def applyFilterFarmer():
    filters = {}

    if request.method == "POST":
        filters['MarketID'] = request.form['MarketID']
        
    collection = chooseCollection('products')

    products = retrieve_products(collection,session['username'])

    productList = []
    marketList = ['']
    
    for product in products:
        if filters['MarketID'] == product['MarketID']:
            productList.append(product)
        marketList.append(product['MarketID'])

    marketList = sorted(list(set(marketList)))

# Get Farmer data
    collection = chooseCollection('users')
    farmerDeets = getFarmData(collection, session['username'])
    farmerList = []
    [farmerList.append(deets) for deets in farmerDeets]    
    farmer = farmerList[0]
    

    return render_template('farmer.html', marketList=marketList, filters=filters, productList=productList, farmer = farmer, user=session['username'], user_status=session['status'])




@app.route('/product_update', methods=['POST'])
def productUpdate():
    
    # Retrieve data from database to display
    collection = chooseCollection('products')
    
    if request.method == "POST":
       

        update_product(collection, request.form['_id'], request.form['product'], request.form['productType'], request.form['units'], request.form['quantity'], request.form['price'])     

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
        delete_product(collection,request.form['_id'])
        products = retrieve_products(collection,session['username'])
        productList = []

        for product in products:
            productList.append(product)
     
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/product_delete_cart', methods=['POST'])
def productDelete_shoppingCart():   
    # Retrieve data from database to display
    collection = chooseCollection('shoppingCart')
    
    if request.method == "POST":
        print (request.form['_id'])
        delete_shoppingCart_product(collection,request.form['_id'])
        shoppingCart_products = retrieveShoppingCart(collection,session['username'])
        shoppingCartList = []

        for product in shoppingCart_products:
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
        
        data = dict(request.form)

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/farmer_home')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            if data['_id'][0] == 'profPic':
                file.save(os.path.join(UPLOAD_FOLDER, session['username']+'_profile.'+filename.rsplit('.', 1)[1].lower()))
                
                collection = chooseCollection('users')
                image = 'file_uploads/'+session['username']+'/'+session['username']+'_profile.'+filename.rsplit('.', 1)[1].lower()
                update_prof_pic(collection, session['username'], image)

            else:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            
                collection = chooseCollection('products')
                image = 'file_uploads/'+session['username']+'/'+filename
                update_image(collection, data['_id'][0], image)
            
            flash('File uploaded succesfully!')
            return redirect('/farmer_home')


@app.route('/shop_produce', methods=['POST','GET'])
def shop_produce():

    collection = chooseCollection('products')

    # Retrieve all products from the database
    all_produce = retrieve_all_produce(collection)
    
    # gathering all of the produce listed in database
    produceList = []

    # gathing all of the products, productypes, units, 
    ProductList = []
    ProductTypeList = []
    marketList = []

    for produce in all_produce:
        produceList.append(produce)
        ProductList.append(produce['Product'])
        ProductTypeList.append(produce['Product Type'])
        marketList.append(produce['MarketID'])
        print(produce['ProducerID'])

    # getting unique values and sorting in alphabetical order
    ProductList = sorted(list(set(ProductList)))
    ProductTypeList = sorted(list(set(ProductTypeList)))
    marketList = sorted(list(set(marketList)))
    # Populate the filters with empty values
    filters = {}
    filters['product'] = ''
    filters['productType'] = ''
    filters['MarketID'] = ''


    return render_template('shop_produce.html', produceList=produceList, ProductList=ProductList, ProductTypeList= ProductTypeList,\
        marketList=marketList, filters=filters, user=session['username'], user_status=session['status'])

@app.route('/apply-filter', methods=['POST'])
def applyFilter():
    
    filters = {}

    if request.method == "POST":

        filters['product'] = request.form['product']
        filters['productType'] = request.form['productType']
        filters['MarketID'] = request.form['MarketID']

    # count number of filters in use, to be used for conditionals below
    count = 0
    for key in filters:
        if filters[key] != '':
            count +=1

    collection = chooseCollection('products')

    # Retrieve all products from the database
    all_produce = retrieve_all_produce(collection)
    
    # gathering all of the produce listed in database
    produceList = []

    # gathing all of the products, productypes, units, 
    ProductList = ['']
    ProductTypeList = ['']
    marketList = ['']

    # loop to determin what information will be presented based on filters
    for produce in all_produce:
        # condition all filters are blank
        if count == 0:
        
            produceList.append(produce)

        # condition for one filter used
        if count == 1:
            if (filters['MarketID'] == produce['MarketID'] or filters['product'] == produce['Product'] or \
                filters['productType'] == produce['Product Type']):
                
                produceList.append(produce)

        # condition for two filters used
        if count ==2 :
            if (filters['MarketID'] == produce['MarketID'] and filters['product'] == produce['Product']) or \
            (filters['MarketID'] == produce['MarketID'] and filters['productType'] == produce['Product Type']) or \
            (filters['product'] == produce['Product'] and filters['productType'] == produce['Product Type']):
                
                produceList.append(produce)

        # condition for all filters used
        if count == 3:
            if (filters['MarketID'] == produce['MarketID'] and filters['product'] == produce['Product'] and \
                filters['productType'] == produce['Product Type']):
                
                produceList.append(produce)
        
        ProductList.append(produce['Product'])
        ProductTypeList.append(produce['Product Type'])
        marketList.append(produce['MarketID'])

    # getting unique values and sorting in alphabetical order
    ProductList = sorted(list(set(ProductList)))
    ProductTypeList = sorted(list(set(ProductTypeList)))
    marketList = sorted(list(set(marketList)))
    
    return render_template('shop_produce.html', produceList=produceList, ProductList=ProductList, ProductTypeList= ProductTypeList,\
        marketList=marketList, filters=filters, user=session['username'], user_status=session['status'])

@app.route('/shopping_cart', methods=['GET','POST'])
def shopping_cart():

    collection = chooseCollection('shoppingCart')
    contents = retrieveShoppingCart(collection, session['username'])

    cartList = []
    for item in contents:
        cartList.append(item)

    # temp = {}
    # for d in cartList:
    #     if d['Product_id'] not in temp:
    #         temp[d['Product_id']] = {}
    #         temp_d = temp[d['Product_id']]
    #         temp_d['Price'] = float(temp_d.get('Price', 0)) + float(d['Price'])
    
    # print(temp)

    return render_template('cart.html', cartList=cartList, user=session['username'], user_status=session['status'])


# ADD HERE FUNCTION TO REMOVE
    collection = chooseCollection('products')
    # deductFromInventory()



@app.route('/add_to_shopping_cart', methods=['GET','POST'])
def add_to_shopping_cart():
    
    if request.method == "POST":
        product = request.form['product']
        productType = request.form['productType']
        marketID = request.form['marketID']
        # have to extract units from request.form since text before
        units = request.form['units']
        # have to extract price from request.form since text before
        price = request.form['price']
        price_float = float(request.form['price'])

        product_id = request.form['product_id']
        ProducerID = request.form['ProducerID']
        quantity = int(request.form['quantity'])
        totalPrice_float = price_float * quantity
        totalPrice_str = '{0:.2f}'.format(price_float*quantity)

        collection = chooseCollection('shoppingCart')

    # Check if the product is already in the cart
        check = checkShoppingCart(collection, session['username'], product_id)
        if check == []:
        # Insert to shopping cart
            insertToShoppingCart(collection, session['username'], product_id, ProducerID, product, productType, units, price, quantity, marketID, totalPrice_float)
        else:
        # Already in there, so we add to the quantity
            incrementInShoppingCart(collection, session['username'], product_id, quantity, totalPrice_float)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}     


@app.route('/make_reservation', methods=['GET','POST'])
def make_reservation():

    if request.method == "POST":
        json_data = request.form['reserved_list']
        data_list = json.loads(json_data)


# ################ NEW RESERVATION SYSTEM #################################

# #### Keeping this until we fix it for the consumer interface as well ####

        sorted_data_list = sorted(data_list, key = lambda i: i['ProducerID'])

    # List producers in the order
        producers = []
        for item in sorted_data_list:
            producers.append(item['ProducerID']) 
        producers = list(set(producers))
        
        print('producers')
        print(producers)

        reservations = []
        for producer in producers:
            stuff = []
            for item in sorted_data_list:
                if item['ProducerID'] == producer:
                    totalPrice = '{0:.2f}'.format(float(item['price'])*float(item['quantity']))
                    stuff.append({"Product":item['product'], "Product Type":item['productType'], "Units":item['units'], "Price":item['price'], "Quantity":item['quantity'], "Total Price":totalPrice})
    
            collection = chooseCollection('reservationsDict')
            insertDictToReservations(collection, {"Username":session['username'], "ProducerID":producer, "MarketID":item['marketID'], "Stuff":stuff})


    
            
# ################ NEW RESERVATION SYSTEM #################################

        for item in data_list:
            product = item['product']
            productType = item['productType']
            units = item['units']
            price = item['price']
            marketID = item['marketID']
            ProducerID = item['ProducerID']
            totalPrice = item['totalPrice']

            '$'+'{0:.2f}'.format(float(item['quantity']) * float(item['price'][1:]))

            quantity = item['quantity']
        


        # Adds reservation to database 
            collection = chooseCollection('reservations')
            insertToReservations(collection, session['username'], ProducerID, product, productType, units, price, marketID, totalPrice, quantity)

        # Empties the shopping cart when reservation is placed
            collection = chooseCollection('shoppingCart')
            emptyShoppingCart(collection, session['username'])

    return redirect('/reservations')
    
@app.route('/reservations', methods=['GET','POST'])
def reservations():
    
    collection = chooseCollection('reservations')
    contents = retrieveShoppingCart(collection, session['username'])

    reservedList = []
    for item in contents:
        reservedList.append(item)

    return render_template('reservations.html', reservedList=reservedList, user=session['username'], user_status=session['status'])


@app.route('/reserved_produce', methods=['GET','POST'])
def reserved_produce():

    # IMPORTANT in this case we pass the username of the farmer, 
    # but in the back we check for the "ProducerID" that matches it!
    collection = chooseCollection('reservationsDict')
    orders = retrieveDictReservations(collection, session['username'])    

    orderList = []
    for order in orders:
        orderList.append(order)

    print(orderList)

    filters ={}
    return render_template('reserved_produce.html', orderList=orderList, filters=filters, user=session['username'], user_status=session['status'])    


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html', user=session['username'], user_status=session['status']), 404