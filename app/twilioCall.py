# import sys
# from twilio.rest import Client

import twilio
from twilio.rest import Client

# Surya's
account_sid = "AC9629dc758c9d995440c7b90b5542d86c"
auth_token  = "b13ff78cc4235ddbabcf41decd4269ee"

# Dimitri's
# account_sid = "ACff10142c492b50031ea0a3b547b820fb"
# auth_token = "6c76d053646b3a58f7bb743495046298"

client = Client(account_sid, auth_token)


def producer_reservation_notification(ProducerID, telephone, username, products):
	
	produce = ""
	for product in products:
		produce = '\n' + produce + product['Quantity'] + ' ' + product['Product']
	message = client.messages.create(
	    to=telephone, 
	    from_="+17797747983",
	    body="Hey " + ProducerID + ", "+ username +" has reserved: "
	    		+ produce 
				+ "\nWoohooo!!!"
				+ "\nGet the full details at https://nearfarms.com/")
	
	print(message.sid)
