from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()
from config import set_up_logger
set_up_logger()
encryption_key: str | None | bytes = os.getenv('ENCRYPTION_KEY')
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

if not encryption_key:
    logger.error("Encryption key is missing kindly insert the encryption key in .env file.")
    os._exit(1)
try:
    encryption_key = encryption_key.encode()   
    cipher = Fernet(encryption_key)
except Exception as e:
    logger.error(f"Invalid encryption key: {e}")
    os._exit(1)

def encrypt_data(data):
    try:
        encrypted_string = cipher.encrypt(data.encode('uft-8'))
        return encrypted_string
    except Exception as e:
        print(f"Error encrypting data: {e}")

def decrypt_data(data):
    try:
        decrypted_string = cipher.decrypt(data).decode('utf-8')
        return  decrypted_string
    except Exception as e:
        print(f"Error decrypting data: {e}")