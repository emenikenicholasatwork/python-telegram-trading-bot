from config import set_up_logger
from database_utils import get_private_key_from_db, save_user_credentials
set_up_logger()
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.rpc.requests import GetBalance

def create_solana_wallet(userid: int) -> any: # type: ignore
    address = get_private_key_from_db(userid)
    if address:
        logger.info("user wallet already exist")
        return address
    else:
        keypair = Keypair()
        pub = keypair.pubkey()
        try:
            save_user_credentials(userid, str(keypair), str(pub))
            return pub
        except Exception as e:
            logger.error(f"Error while saving credentials: {e}")

def get_balance(address):
    try:
        pub_key = Pubkey.from_string(address)
        balance = GetBalance(pub_key).to_json() # type: ignore
        return balance
    except Exception as e:
        logger.info(f"Error fetching balance: {e}")
        
        

def get_sol_in_dollar():
    return ""