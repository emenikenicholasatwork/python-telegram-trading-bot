from config import set_up_logger
from database_utils import get_private_key_from_db, save_user_credentials
set_up_logger()
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
from solders.keypair import Keypair

def create_solana_wallet(userid: int) -> any: # type: ignore
    p_key = get_private_key_from_db(userid)
    if p_key:
        logger.info("user wallet already exist")
        return p_key
    else:
        keypair = Keypair()
        pub = keypair.pubkey()
        try:
            save_user_credentials(userid, str(keypair), str(pub))
            return pub
        except Exception as e:
            logger.error(f"Error while saving credentials: {e}")



async def get_solana_wallet_balance():
    return ""

def get_sol_in_dollar():
    return ""