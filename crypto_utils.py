# importing the required packages for the file
import asyncio
import ccxt

# initialising the binance exchange
exchange = ccxt.binance()

# asynchronous function to get the price of coin
async def fetch_coin_price(coin_name):
    # trying the request in case of errors
    try:
        # running the request in another thread to save time
        ticker = await asyncio.to_thread(exchange.fetch_ticker, coin_name+"/USDT")
        return ticker['last']
    except Exception as e:
        # returning the encountered error
        return f"Error fetching {coin_name} price"

# asynchronous function to get the price of sol
async def fetch_solana_price():
    # trying the request in case of errors
    try:
        # running the request in another thread to save time
        ticker = await asyncio.to_thread(exchange.fetch_ticker, "SOL/USDT")
        return ticker['last']
    except Exception as e:
        # returning the encountered error
        return "Error fetching Sol price"

# asynchronous function to get the price of btc
async def fetch_bitcoin_price():
    # trying the request in case of errors
    try:
        # running the request in another thread to save time
        ticker = await asyncio.to_thread(exchange.fetch_ticker, "BTC/USDT")
        return ticker['last']
    except Exception as e:
        # returning the encountered error
        return "Error fetching Btc price"

# asynchronous function to get the price of eth
async def fetch_ethereum_price():
    # trying the request in case of errors
    try:
        # running the request in another thread to save time
        ticker = await asyncio.to_thread(exchange.fetch_ticker, "ETH/USDT")
        return ticker['last']
    except Exception as e:
        # returning the caught error
        return "Error fetching Eth price"