from database_utils import setup_db
from bot import BOT

def start_bot():
    setup_db()
    BOT()

if __name__ == "__main__":
    start_bot()

