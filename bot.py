#importing the required packages
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from crypto_utils import fetch_coin_price, fetch_bitcoin_price, fetch_solana_price, fetch_ethereum_price
from wallet_utils import create_solana_wallet, get_solana_wallet_balance, get_sol_in_dollar

#loading the dotenv file
load_dotenv()

#geting the bot token from the .env file
BOT_TOKEN=os.getenv('BOT_TOKEN')

# bot state to regulate the user inputs
BUY_TOKEN_NAME = 1

class BOT:
    def __init__(self):
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.button_clicked))
        application.add_handler(MessageHandler(filters.TEXT, self.user_reply))
        application.run_polling(poll_interval=5)

    # a start function to handle the user start command
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # getting all the required variables
        sol_price = await fetch_solana_price()
        btc_price = await fetch_bitcoin_price()
        eth_price = await fetch_ethereum_price()
        solana_wallet = await create_solana_wallet()
        solana_wallet_balance = await get_solana_wallet_balance()
        solana_in_dollar = get_sol_in_dollar()

        # inline keyboard for the start menu
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

        # formatted text to be return when button is clicked
        text = (f"<b>SOL</b>: ${sol_price}=<b>BTC</b>: ${btc_price}=<b>ETH</b>: ${eth_price}"
                f"<b>Trading Bot Official</b>"
                f"Here is your Solana wallet. Fund your Wallet and start trading."
                f"🅴 Your Solana Wallet:"
                f"<code>{solana_wallet}</code> (Tap to copy)"
                f"Balance: {solana_wallet_balance} SOL ${solana_in_dollar}"
                f""
                f"💡 Enter a token address to quickly open the buy menu."
                )
        # code to make reply to user
        await update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode="HTML")

    # function to take care of the callbacks when any button is clicked by the user
    async def button_clicked(self, update: Update, context: CallbackContext) -> None:
        # variable to hold the callback data from the update
        query = update.callback_query
        # perform some checks on the query data to know the operation the user wants to perform
        if query.data == 'buy':
            context.user_data['state'] = BUY_TOKEN_NAME
            await query.message.reply_text(text="✏️ Enter the token to buy and base token e.g BTC/USDT : ", reply_markup=ForceReply())


    # function to take care of user replys i.e all user replys in TEXT format
    async  def user_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # perform some checks on the state to know what the user is replying to
        if context.user_data['state'] == BUY_TOKEN_NAME:
            # trying the buy function
            try:
                pass
            except Exception as e:
                print(f"Error while trying to buy token: {e}")


    # function to take care of coin purchase i.e buying token by the bot
    async def buy_token(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # getting the coin name from the user reply i.e update
        token_name = update.message.text
        # trying to get coin price
        try:
            # token price
            token_price = await fetch_coin_price(token_name)
            if token_price:
                pass
            else:
                pass
        except Exception as e:
            print(f"Error while trying to buy token: {e}")