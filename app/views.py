import os
from flask import render_template, redirect, request
from app import app, models
from .forms import ProductForm
from .models import *
from werkzeug import secure_filename
# Access the models file to use SQL functions


@app.route('/')
def index():
    return redirect('/home')
    #return redirect('/farmer_home')

@app.route('/home', methods=['GET'])
def home():
    
    return render_template('home.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    productForm = ProductForm()
    if productForm.validate_on_submit():
        # Get data from the form
        # Send data from form to Database
        product = productForm.product.data
        productType = productForm.productType.data
        subType = productForm.subType.data
        quantity = productForm.quantity.data
        price = productForm.price.data
        image = productForm.image.data

        collection = chooseCollection('products')
        insert_products(collection, product, productType, subType, quantity, price, image)

        return redirect('/farmer_home')
    return render_template('product.html', productForm=productForm)

@app.route('/farmer_home', methods=['GET'])
def farmer_home():
    # Retreive data from database to display
    collection = chooseCollection('products')
    products = retrieve_all(collection)

    productList = []

    for product in products:
        productList.append(product)

    return render_template('farmer.html', productList=productList)

@app.route('/consumer_home', methods=['GET'])
def consumer_home():
    
    pass

    #UNCOMMENT when template is created
    # return render_template('consumer.html')

@app.route('/file_upload', methods = ['GET', 'POST'])
def file_upload():

    UPLOAD_FOLDER = '/file_uploads/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### NEED TO FIX ALL THE RETURN FIELDS IN THE FOLLOWING CODE

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return '''<!doctype html><p>BOB</p>'''#redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return '''<!doctype html><p>BOB</p>''' #redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, filename))
            #file.save(os.path.join(UPLOAD_FOLDER, filename))
            return '''<!doctype html><p>BOB</p>'''#redirect(url_for('uploaded_file',
                                    #filename=filename))
    
