from solana.rpc.async_api import AsyncClient
import requests
from config import set_up_logger
from database_utils import get_private_key_from_db, save_user_credentials
set_up_logger()
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
from solders.keypair import Keypair
from solders.pubkey import Pubkey

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


async def get_sol_balance(address) -> any: # type: ignore
    try:
        async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
            pub_key = Pubkey.from_string(address)
            balance_in_lamports = await client.get_balance(pub_key)
            balance_in_sol = balance_in_lamports / 1_000_000_000 # type: ignore
            return balance_in_sol
    except Exception as e:
        logger.info(f"Error fetching balance: {e}")
        
def convert_sol_to_dollar(sol):
    coingecko_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    response = requests.get(coingecko_api_url)
    sol_to_usd_rate = response.json()['solana']['usd']
    balance_in_usd = sol * sol_to_usd_rate
    return balance_in_usd
        

def get_sol_in_dollar():
    return ""