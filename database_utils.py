# importing the required packages for the file
import sqlite3
from sqlite3 import connect
from wallet_utils import decrypt_data

# function to check if the database needs to be created
def setup_db():
    try:
        # connecting to the database or create if it does not exist
        connection = sqlite3.connect("users.db")
        # creating a cursor to interact with the database
        cursor = connection.cursor()

        # create a new table
        cursor.execute('''
         CREATE TABLE IF NOT EXISTS users(
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               telegram_id INTEGER NOT NULL,
               private_key BLOB NOT NULL,
               address TEXT NOT NULL
            )
        ''')
        # committing and closing the connection
        connection.commit()
        connection.close()
    except Exception as e:
        # printing the encountered error
        print(f"Error while setting up the database: {e}")

# function to get user private key from database
def get_private_key_from_db(telegram_user_id):
    # trying the process in case of errors
    try:
        # making connection and getting the cursor for the query
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        # defining and executing thr query
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_user_id} LIMIT 1;"
        cursor.execute(query)
        # returning the row filled with user query expectations and closing the connection
        row = cursor.fetchone()
        connection.close()
        # returning the third item on the query row i.e user private key
        if row:
            return decrypt_data(row[2])
        return None
    except Exception as e:
        # printing the encountered error
        print(f"Error fetching the private key: {e}")

# function to get user wallet address from database
def get_wallet_address_from_db(telegram_user_id):
    # trying the process in case of errors
    try:
        # making connection to the db and getting the cursor for the query
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        # defining and executing query
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_user_id} LIMIT 1;"
        cursor.execute(query)
        # returning the row filled with user query expectations and closing the connection
        row = cursor.fetchone()
        connection.close()
        # returning the fourth item on the query row i.e user address
        if row:
            return row[3]
        return None
    except Exception as e:
        # printing the encountered error
        print(f"Error fetching address from db: {e}")

# function to save user credentials to the db
def save_user_credentials(telegram_id, private_key, wallet_address):
    # trying the process in case of errors
    try:
        # making connection to the db and getting the cursor for the query
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        # executing the query directly
        cursor.execute("INSERT INTO users (telegram_id, private_key, address) VALUES (?, ?, ?)", (telegram_id, private_key, wallet_address))
        # commit and close the connection after insertion
        connection.commit()
        connection.close()
    except Exception as e:
        # printing the encountered error
        print(f"Error saving user credentials to db: {e}")