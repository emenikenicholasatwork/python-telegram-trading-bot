import logging
from decimal import Decimal
import ccxt

from config import set_up_logger
set_up_logger()
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
exchange = ccxt.bitfinex2()

async def fetch_coin_price(coin_name: str) -> None | str | float | int | Decimal:
    try:
        logger.info(f"Fetching {coin_name} price")
        ticker = exchange.fetch_ticker(coin_name+"/USDT")
        if 'last' in ticker:
            price = ticker['last']
            logger.info(f"Returning price for {coin_name}: {price}")
            return price
        else:
            logger.error(f"Ticker data for {coin_name} does not contain 'last' price")
            return ""
    except Exception as e:
        logger.error(f"Failed to fetch {coin_name} price. Error: {e}")
        return None