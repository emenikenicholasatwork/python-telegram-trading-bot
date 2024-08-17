#
###
# This file kick-start the bot and setup the database.
###
#

# importing packages that will be required to setup the bot
from database_utils import setup_db
from bot import BOT

# function to create a new instance of the bot
def start_bot():
    setup_db()
    BOT()


# starting the bot when script is started
if __name__ == "__main__":
    start_bot()

