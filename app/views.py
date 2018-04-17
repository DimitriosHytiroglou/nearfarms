import os
from flask import session, render_template, redirect, request, flash
from app import app, models
from .forms import *
from .models import *
from werkzeug import secure_filename
from app.encryption.HashingHandler import *
# Access the models file to use SQL functions


@app.route('/')
def index():
    return redirect('/home')
    #return redirect('/farmer_home')

@app.route('/home', methods=['GET'])
def home():
    
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')

# App routing for USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    
    wrong = 'none'

    if loginForm.validate_on_submit():
        
        u = loginForm.username.data
        p = loginForm.password.data
        t = loginForm.userType.data

        collection = chooseCollection('users')
        userPass = getUserPass(collection, u)

        if userPass != []:
            if checkPass(userPass,p):
                session['username'] = u
                session['password'] = userPass
                if t == 'Producer':
                    return redirect('/farmer_home')
                elif t == 'Consumer':
                    return redirect('/consumer_home')
            else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong)
        else:
                wrong = 'block'
                return render_template('login.html', loginForm=loginForm, wrong=wrong)

    return render_template('login.html', loginForm=loginForm, wrong=wrong)




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

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertUser(collection, email, username, password, first_name, last_name, farm_name, farm_description)

            session['username'] = username
            session['password'] = password

            # Create directory to save images of this producer
            if not os.path.exists('file_uploads/'+username):
                os.makedirs('file_uploads/'+username)

            return redirect('/farmer_home') 


        else:
            wrong = 'block'
            return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong)

    return render_template('register_producer.html', newProducerForm=newProducerForm, wrong=wrong)


# App routing to CREATE USER
@app.route('/create_newConsumer', methods=['GET', 'POST'])
def create_newConsumer():
    
    wrong = 'none'

    newConsumerForm = newConsumerForm()
    if newConsumerForm.validate_on_submit():
        first_name = newConsumerForm.first_name.data
        last_name = newConsumerForm.last_name.data
        email = newConsumerForm.email.data
        username = newConsumerForm.username.data
        password = newConsumerForm.password.data

        collection = chooseCollection('users')
        userPass = getUserPass(collection, username)

        if userPass == []:
            # Password Hashing
            password = hashPass(password)

            collection = chooseCollection('users')
            insertUser(collection, email, username, password, first_name, last_name)

            session['username'] = username
            session['password'] = password

            return redirect('/consumer_home')

        else:
            wrong = 'block'
            return render_template('register_consumer.html', newConsumerForm=newConsumerForm, wrong=wrong)

    return render_template('register_consumer.html', newConsumerForm=newConsumerForm, wrong=wrong)



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
        # image = productForm.image.data

        collection = chooseCollection('products')
        insert_products(collection, producerID, product, productType, subType, quantity, price)

        return redirect('/farmer_home')
    return render_template('product.html', productForm=productForm, user=session['username'])

@app.route('/farmer_home', methods=['GET'])
def farmer_home():
    # Retreive data from database to display
    collection = chooseCollection('products')
    
    #products = retrieve_all(collection)

    products = retrieve_products(collection,session['username'])

    productList = []

    for product in products:
        productList.append(product)

    return render_template('farmer.html', productList=productList, user=session['username'])

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
            #return render_template('product.html', **templateData)
            #return '''<!doctype html><p>BOB</p>'''#redirect(request.url)
            return redirect('/farmer_home')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            #return render_template('product.html', **templateData)
            #return '''<!doctype html><p>BOB</p>''' #redirect(request.url)
            return redirect('/farmer_home')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.root_path, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded succesfully!')
            return redirect('/farmer_home')
            #return render_template('product.html', **templateData)
            #return '''<!doctype html><p>BOB</p>'''#redirect(url_for('uploaded_file',
                                    #filename=filename))

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

    return render_template('shop_produce.html', produceList=produceList, ProductList=ProductList, ProductTypeList= ProductTypeList,\
        SubTypeList=SubTypeList, user=session['username'])
   
