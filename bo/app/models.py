import pymongo

# gets you the handler on the mongo client
client = pymongo.MongoClient()
# choose the database
db = client.nearfarms

# Choose Collection
def chooseCollection(collectionChoice):
    collection = db[collectionChoice]
    return collection

# insert value
def insert_products(collection, product, productType, subType, quantity, price, image):
    collection.insert({'Product':product, 'Product Type':productType, 'Sub Type':subType,'Quantity':quantity, 'Price':price, 'Image':image})

def retrieve_all(collection):
    return collection.find()