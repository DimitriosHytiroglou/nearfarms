import pymongo

####### DEPRECATING LOCAL STORAGE ########
# gets you the handler on the mongo client
#client = pymongo.MongoClient()
# choose the database
#db = client.nearfarms
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#


######### Adding REMOTE STORAGE ##########
# Connects to MongoDB Atlas Database
# and gets you the handler on the mongo client
# The connection string format is "mongodb://ClusterName:Password@AllClusterShards"
client = pymongo.MongoClient("mongodb://nearfarmsapp:grannysmithsapples@nearfarmscluster-shard-00-00-uoq95.mongodb.net:27017,nearfarmscluster-shard-00-01-uoq95.mongodb.net:27017,nearfarmscluster-shard-00-02-uoq95.mongodb.net:27017/megalab?ssl=true&replicaSet=NearFarmsCluster-shard-0&authSource=admin")
# ---TODO---> Must change password to be taken from hashed value on database and not stored in a string like this

#Choose database
db = client.megalab

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



# # # CONSUMERS # # #




# # # PRODUCERS # # #

# Insert Producer
def insertUser(collection, email, username, password, first, last, farm, description):
	collection.insert({"Email":email, "Username":username, "Password":password, "First":first, "Last":last, "Farm":farm, "description":description})

# insert value
def insert_products(collection, producerID, product, productType, subType, quantity, price, image):
    collection.insert({'ProducerID':producerID, 'Product':product, 'Product Type':productType, 'Sub Type':subType,'Quantity':quantity, 'Price':price, 'Image':image})

def retrieve_products(collection, username):
	products = collection.find({'ProducerID':username})
	if products.count() is not 0:
		return products
	else:
		return []

### WHAT IS THIS? LETS GIVE IT A NAME AND CATEGORIZE IT

def retrieve_all(collection):
    return collection.find()
