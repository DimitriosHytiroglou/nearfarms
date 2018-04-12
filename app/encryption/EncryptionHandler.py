# This module handels emcryption with a key.
#It is NOT used in this implementation

##https://pypi.python.org/pypi/simple-crypt
#https://launchpad.net/pycrypto
##https://stackoverflow.com/questions/9803784/basic-encrypt-and-decrypt-function
##https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password

import Crypto
from simplecrypt import encrypt, decrypt

def main():
	pass

def encryptPass(password):
	ciphertext = encrypt('password', password)
	return ciphertext

def decryptPass(cypher):
	plaintext = decrypt('password', cypher)
	return plaintext


if __name__ == "__main__":
   main()
