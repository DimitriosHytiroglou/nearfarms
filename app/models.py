import pymongo
import bson 

######### Adding REMOTE STORAGE ##########
# Connects to MongoDB Atlas Database
# and gets you the handler on the mongo client
# The connection string format is "mongodb://ClusterName:Password@AllClusterShards"
client = pymongo.MongoClient("mongodb://nearfarmsapp:grannysmithsapples@nearfarmscluster-shard-00-00-uoq95.mongodb.net:27017,nearfarmscluster-shard-00-01-uoq95.mongodb.net:27017,nearfarmscluster-shard-00-02-uoq95.mongodb.net:27017/megalab?ssl=true&replicaSet=NearFarmsCluster-shard-0&authSource=admin")
# ---TODO---> Must change password MongodDB Atlas to be taken from hashed value on database and not stored in a string like this

#Choose database
db = client.nearfarms

# # # GENERAL # # #

# Choose Collection
def chooseCollection(collectionChoice):
    collection = db[collectionChoice]
    return collection

# Retrieve a users password
def getUserPass(collection, username):
	friends = collection.find({'Username':username})
	if friends.count() is not 0:
		return str(friends[0]['Password'])
	else:
		return []

# Get Logged In user's type (Producer/Consumer)
def getUserType(collection, username):
	types = collection.find({'Username':username})
	if types.count() is not 0:
		print(str(types[0]['User Type']))
		return str(types[0]['User Type'])
	else:
		return []

# # # CONSUMERS # # #

# returns all of the produce in database to display for the consumer !!! WILL NEED TO DELINEATE BY MARKET EVENTUALLY
def retrieve_all_produce(collection):
    return collection.find()

# Create new consumer entry in database
def insertConsumer(collection, email, username, password, first, last, userType, image):
	collection.insert({"Email":email, "Username":username, "Password":password, "First":first, "Last":last, "User Type":userType, "Image":image})

# Retrieve all consumer data
def getConsumerData(collection, username):
	consumer_data = collection.find({'Username':username})
	return consumer_data

# Update existing consumer
def update_consumer(collection, _id, email, first, last):
	idb = bson.ObjectId(_id)
	collection.update_one({"_id": idb }, {"$set": {"Email":email, "First":first, "Last":last}})	



# # # SHOPPING CART # # #

# Insert product to shopping cart
def insertToShoppingCart(collection, username, product_id, ProducerID, product, productType, units, price, quantity, marketID, totalPrice):
	collection.insert({"Username":username, "Product_id":product_id, "ProducerID":ProducerID, "Product":product, "Product Type":productType, "units":units,"Price":price, "Quantity":quantity, "marketID":marketID, "totalPrice":totalPrice})

# Increment quantity of product in shopping cart
def incrementInShoppingCart(collection, username, product_id, quantity, totalPrice):
	collection.update_one({"Username":username, "Product_id":product_id}, {"$inc": {'Quantity':quantity, 'totalPrice':totalPrice}})	

# Retrieve shopping cart contents
def retrieveShoppingCart(collection, username):
	contents = collection.find({'Username':username})
	if contents.count() is not 0:
		return contents
	else:
		return []

# Check if the product is already in the cart
def checkShoppingCart(collection, username, product_id):
	contents = collection.find({'Username':username, "Product_id":product_id})
	if contents.count() is not 0:
		return contents
	else:
		return []

# Empty user's shopping cart
def emptyShoppingCart(collection, username):
	collection.delete_many({"Username":username })

# # # RESERVATIONS # # #


# ###### Deprecated system ######

# def insertToReservations(collection, username, ProducerID, product, productType, units, price, marketID, totalPrice, quantity):
# 	collection.insert({"Username":username, "ProducerID":ProducerID, "Product":product, "Product Type":productType, "units":units,"Price":price, "marketID":marketID, "totalPrice":totalPrice, "Quantity":quantity})

# def retrieveReservations(collection, username):
# 	contents = collection.find({'Username':username})
# 	if contents.count() is not 0:
# 		return contents
# 	else:
# 		return []

# ###### Deprecated system ######


# ##### NEW RESERVATION SYSTEM FUNCTIONS #########

# Insert reservation to system
def insertDictToReservations(collection, order):
	collection.insert(order)


# Retrieve a producer's reservations
def retrieveProducerReservations(collection, ProducerID):
	contents = collection.find({'ProducerID':ProducerID})
	if contents.count() is not 0:
		return contents
	else:
		return []

# Retrieve a consumer's reservations
def retrieveConsumerReservations(collection, username):
	contents = collection.find({'Username':username})
	if contents.count() is not 0:
		return contents
	else:
		return []

# Fulfill Order
def fulfillOrder(collection, order_id):
	_id = bson.ObjectId(order_id)
	collection.update_one({"_id": _id }, {"$set": {'Fulfilled':'Yes'}})	


# ##### NEW RESERVATION SYSTEM FUNCTIONS #########


# # # PRODUCERS # # #

# Insert Producer
def insertProducer(collection, email, username, password, first, last, telephone, farm, description, userType, image):
	collection.insert({"Email":email, "Username":username, "Password":password, "First":first, "Last":last,"Telephone":telephone , "Farm":farm, "description":description, "User Type":userType, 'Image':image})

# Retrieve all Producer data
def getFarmData(collection, username):
	farm_data = collection.find({'Username':username})
	return farm_data

# Update producer prof pic
def update_prof_pic(collection, username, image):
	collection.update_one({"Username": username }, {"$set": {'Image':image}})	
	

# # # PRODUCTS # # #

# Insert new product
def insert_products(collection, producerID, product, productType, units, quantity, price, image, marketID):
    collection.insert({'ProducerID':producerID, 'Product':product, 'Product Type':productType, 'units':units,'Quantity':quantity, 'Price':price, 'Image':'','MarketID':marketID})

# Retrieve all of producer's products
def retrieve_products(collection, username):
	products = collection.find({'ProducerID':username})
	if products.count() is not 0:
		return products
	else:
		return []

# Update existing product
def update_product(collection, _id, product, productType, units, quantity, price):
	idb = bson.ObjectId(_id)
	collection.update_one({"_id": idb }, {"$set": {'Product':product, 'Product Type':productType, 'units':units,'Quantity':quantity, 'Price':price}})	
#  https://codehandbook.org/pymongo-tutorial-crud-operation-mongodb/\

def deductFromInventory(collection, _id, amount):
	idb = bson.ObjectId(_id)
	# collection.update_one({"_id": idb }, {"$set": {'Quantity':}})

# Delete existing product
def delete_product(collection, _id):
	idb = bson.ObjectId(_id)
	collection.delete_one({"_id": idb })	

# Delete item from shoppingCart
def delete_shoppingCart_product(collection, _id):
	idb = bson.ObjectId(_id)
	collection.delete_one({"_id": idb })	


# Update existing product's image
def update_image(collection, _id, image):
	idb = bson.ObjectId(_id)
	collection.update_one({"_id": idb }, {"$set": {'Image':image}})	
	