# importing all the packages required for the file
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()
encryption_key = os.getenv('ENCRYPTION_KEY')

# function to encrypt data
def encrypt_data(data):
    # first trying the process in case of errors
    try:
        # creating a fernet instance with the encryption key
        cipher = Fernet(encryption_key)
        # encrypt the data with the fernet instance and return the value
        encrypted_string = cipher.encrypt(data.encode('uft-8'))
        return encrypted_string
    except Exception as e:
        # printing the encountered error
        print(f"Error encrypting data: {e}")

# function to decrypt data
def decrypt_data(data):
    # first trying the process in case of errors
    try:
        # creating an instance of Fernet with the private key
        cipher = Fernet(encryption_key)
        # decrypt the data with fernet instance and return the value
        decrypted_string = cipher.decrypt(data).decode('utf-8')
        return  decrypted_string
    except Exception as e:
        # printing the encountered error
        print(f"Error decrypting data: {e}")