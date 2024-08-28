import solana
from solana.rpc.async_api import AsyncClient
import requests
import solana.utils
from config import set_up_logger
from database_utils import get_private_key_from_db, save_user_credentials
set_up_logger()
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from spl.token.async_client import AsyncToken
program_id = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

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


async def get_sol_balance(address) -> any:  # type: ignore
    try:
        async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
            pub_key = Pubkey.from_string(address)
            balance_response = await client.get_balance(pub_key)
            balance_in_lamports = balance_response.value
            balance_in_sol = balance_in_lamports / 1_000_000_000
            sol_in_dollar = await convert_sol_to_dollar(balance_in_sol)
            return balance_in_sol, sol_in_dollar
    except Exception as e:
        logger.error(f"Error fetching balance: {e}")

        
async def convert_sol_to_dollar(sol):
    coingecko_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        response = requests.get(coingecko_api_url)
        response.raise_for_status()
        sol_to_usd_rate = response.json()['solana']['usd']
        balance_in_usd = sol * sol_to_usd_rate
        return balance_in_usd
    except Exception as e:
        logger.error(f"Error fetching SOL to USD conversion rate: {e}")
        return None
    
async def get_token_details_from_address(address: str):
    logger.info("fetching token details")
    try:
        async with AsyncClient("https://api.minnet-beta.solana.com") as client:
            token_public_key = Pubkey.from_string(address)
            token = AsyncToken(client, token_public_key, program_id=program_id)
            logger.info(token)
    except Exception as e:
        logger.error(f"Error fetching token details: {e}")
        return None