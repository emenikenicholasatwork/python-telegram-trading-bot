# importing the required packages for the file
import sqlite3
from sqlite3 import connect

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
               user_id INTEGER PRIMARY KEY,
               telegram_id INTEGER NOT NULL,
               private_key BLOB NOT NULL,
               address TEXT NOT NULL
            )
        ''')
        # committing and closing the connection
        connection.commit()
        connection.close()
    except Exception as e:
        print("Error while setting up the database")

# function to get user private key from database
def get_private_key_from_db(telegram_user_id):
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        query = f"SELECT * FROM users WHERE telegram_id = {telegram_user_id} LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        connection.close()
        if row:
            return row
        return None
    except Exception as e:
        print("Error fetching the private key from database")