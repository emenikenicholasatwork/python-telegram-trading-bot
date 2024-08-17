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

# writing a start function for the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sol_price = await fetch_solana_price()
    btc_price = await fetch_bitcoin_price()
    eth_price = await fetch_ethereum_price()

    text = (f"<b>SOL</b>: ${sol_price}=<b>BTC</b>: ${btc_price}=<b>ETH</b>: ${eth_price}"
            f"<b>Trading Bot Official</b>"
            f"Here is your Solana wallet. Fund your Wallet and start trading.")
    await update.message.reply_text(text, parse_mode="HTML")


# writing the main function to start the bot
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(poll_interval=5)

# running the main function when the script starts
if __name__ == "__main__":
    main()