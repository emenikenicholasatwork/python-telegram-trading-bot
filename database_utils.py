import sqlite3
from helper_utils import decrypt_data
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def setup_db():
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute('''
         CREATE TABLE IF NOT EXISTS users(
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               telegram_id INTEGER NOT NULL,
               private_key BLOB NOT NULL,
               address TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error while setting up the database: {e}")

def get_private_key_from_db(telegram_user_id):
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_user_id} LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        connection.close()
        if row:
            return decrypt_data(row[2])
        return None
    except Exception as e:
        print(f"Error fetching the private key: {e}")

def get_wallet_address_from_db(telegram_user_id):
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_user_id} LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        connection.close()
        if row:
            return row[3]
        return None
    except Exception as e:
        print(f"Error fetching address from db: {e}")

def save_user_credentials(telegram_id: int, private_key: str, wallet_address: str):
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (telegram_id, private_key, address) VALUES (?, ?, ?)", (telegram_id, private_key, wallet_address))
        connection.commit()
        connection.close()
        logger.info("Successfully saved new user to db")
    except Exception as e:
        logger.error(f"Error saving user credentials to db: {e}")