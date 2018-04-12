# This module handles hashing of the passwords stored in the database

import uuid
import hashlib
 
def main():
	pass

def hashPass(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def checkPass(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
 
if __name__ == "__main__":
   main()