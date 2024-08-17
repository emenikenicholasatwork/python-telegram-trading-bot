#importing the required packages
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from crypto_utils import fetch_coin_price, fetch_bitcoin_price, fetch_solana_price, fetch_ethereum_price

#loading the dotenv file
load_dotenv()

#geting the bot token from the .env file
BOT_TOKEN=os.getenv('BOT_TOKEN')

class BOT:
    def __init__(self):
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", self.start))
        application.run_polling(poll_interval=5)

    # a start function to handle the user start command
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # getting the prices of top coins
        sol_price = await fetch_solana_price()
        btc_price = await fetch_bitcoin_price()
        eth_price = await fetch_ethereum_price()

        text = (f"<b>SOL</b>: ${sol_price}=<b>BTC</b>: ${btc_price}=<b>ETH</b>: ${eth_price}"
                f"<b>Trading Bot Official</b>"
                f"Here is your Solana wallet. Fund your Wallet and start trading."
                f"🅴")

        await update.message.reply_text(text, parse_mode="HTML")
