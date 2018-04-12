from flask import render_template, redirect, request
from app import app, models
from .forms import ProductForm
from .models import *
# Access the models file to use SQL functions


@app.route('/')
def index():
    return redirect('/farmer_home')


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
