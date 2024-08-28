from multiprocessing import process
import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from crypto_utils import fetch_coin_price
from wallet_utils import create_solana_wallet, get_sol_balance, get_token_details_from_address
from config import set_up_logger

set_up_logger()
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
if BOT_TOKEN.__eq__(""):
    logger.error("Bot token is missing. kindly insert token in .env file")
    os._exit(1)
    

BUY_TOKEN_NAME = 1

class BOT:
    def __init__(self):
        logger.info("Initializing bot")
        application = Application.builder().token(BOT_TOKEN).build() # type: ignore
        logger.info("Bot successfully launched.")
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.button_clicked))
        application.add_handler(MessageHandler(filters.TEXT, self.user_reply))
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info("Start command by the user")
        logger.info("fetching price datas")
        userid = update.message.from_user.id # type: ignore
        prices_result = await asyncio.gather(
            fetch_coin_price("SOL"),
            fetch_coin_price("BTC"),
            fetch_coin_price("ETH")
        )
        pub_key = create_solana_wallet(userid)
        sol_price, btc_price, eth_price = prices_result
        solana_balance, sol_in_dollar = await get_sol_balance(pub_key)
        inline_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text='Buy', callback_data='buy'),
                    InlineKeyboardButton(text='Sell', callback_data='sell')
                ],
                [
                    InlineKeyboardButton(text='Positions', callback_data='position'),
                    InlineKeyboardButton(text=' Limit Orders', callback_data='limit_order'),
                    InlineKeyboardButton(text='DCA Orders', callback_data='dca_order')
                ],
                [
                    InlineKeyboardButton(text='Copy Trade', callback_data='copy_trade'),
                    InlineKeyboardButton(text='Sniper', callback_data='snipper'),
                ],
                [
                    InlineKeyboardButton(text='New Pairs', callback_data='new_pairs'),
                    InlineKeyboardButton(text='Bride', callback_data='bride'),
                    InlineKeyboardButton(text='Withdraw', callback_data='withdraw')
                ],
                [
                    InlineKeyboardButton(text='⚙️ Settings', callback_data='settings'),
                    InlineKeyboardButton(text='Help', callback_data='help'),
                    InlineKeyboardButton(text='Refresh', callback_data='refresh')
                ]
            ]
        )

        text = (f"<b>SOL</b>: ${sol_price}=<b>BTC</b>: ${btc_price}=<b>ETH</b>: ${eth_price}"
                f"\n\n"
                f"<b>UniSol - Trading Bot Official\n</b>"
                f"Here is your Solana wallet. Fund your Wallet and start trading.\n"
                f"🅴 Your Solana Wallet:\n"
                f"<code>{pub_key}</code> (Tap to copy)\n\n"
                f"Balance:<code>{solana_balance} SOL (${sol_in_dollar})</code>\n"
                f"💡💡💡💡💡💡💡\n"
                f"Enter a token address to quickly open the buy menu."
                )
        await update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode="HTML") # type: ignore

    async def button_clicked(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        if query.data == 'buy':
            logger.info("buy button clicked")
            context.user_data['state'] = BUY_TOKEN_NAME
            await query.message.reply_text(text="✏️ Enter the token to buy and base token e.g BTC/USDT : ", reply_markup=ForceReply())


    async  def user_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data['state'] == BUY_TOKEN_NAME:
            try:
                text = update.message.text
                await get_token_details_from_address(text)
            except Exception as e:
                print(f"Error while trying to buy token: {e}")


    async def buy_token(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        token_name = update.message.text
        try:
            token_price = await fetch_coin_price(token_name)
            if token_price:
                pass
            else:
                pass
        except Exception as e:
            print(f"Error while trying to buy token: {e}")