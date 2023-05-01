import os

import telebot

import re

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instance of the robot
BOTTOKEN = os.environ['BOTTOKEN']
bot = telebot.TeleBot(BOTTOKEN)

# Initializations
wallet = {}
referral_data = {}
user_airdrop = 60
referred_link = {}
SUCCESS_MESSAGE = os.environ['SUCCESS_MESSAGE']
ERROR_MESSAGE = f"""
👏 Follow <b><a href="https://twitter.com/musheehub">Mushee Twitter</a></b>

👏 Join <b><a href="https://t.me/musheehub">Mushee Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/musheehub">Mushee Telegram Group</a></b>

😒 Connect with us to continue
"""

WALLET_MESSAGE = f"""
🗒️ What is your BEP-20(BSC) wallet address!!?

<b><i> Please submit your Trustwallet or SafePal address. Address must be from a Decentralized crypto platform</i></b>
"""

WELCOME_MESSAGE = f"""
👋 Hello, Old sport! 

🌞 1 MSH = $0.3
⛅ Get <b>50 MSH</b> for joining and completing task
🌬️ Get <b>5 MSH</b> per referral 

📝 Airdrop will end soon...

🔥 Complete the task and be deemed eligible

🗒️ <b>TASK:</b>

👏 Follow <b><a href="https://twitter.com/musheehub">Mushee Twitter</a></b>

👏 Join <b><a href="https://t.me/musheehub">Mushee Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/musheehub">Mushee Telegram Group</a></b>

🧏 Use only positive words to chat in the group otherwise you will miss the big opportunity

<b>NOTE: All tasks are mandatory</b>

<b>You can use Admin referral Link: https://t.me/{bot.get_me().username}?start={1121070064} </b>
"""

# Define the regular expression to match BSC addresses
BSC_ADDRESS_REGEX = r'^0x([A-Fa-f0-9]{40})$'

# Custom define keyboard
home_button = telebot.types.KeyboardButton('🏠 Home')
main_menu = telebot.types.KeyboardButton('💢 Main Menu')
mushee_subscribe = telebot.types.KeyboardButton('🫡 Join us')
register_wallet = telebot.types.KeyboardButton('😌 Wallet')
change_wallet_address = telebot.types.KeyboardButton('📰 Change address')
airdrop_balance = telebot.types.KeyboardButton('🤑 Balance')
referral = telebot.types.KeyboardButton('🧑‍🤝‍🧑 Referrals')

no_custom_keyboard = telebot.types.ReplyKeyboardRemove()
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
home_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
subscribe_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
wallet_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)


main_menu_keyboard.add(register_wallet, airdrop_balance, referral, change_wallet_address)
home_keyboard.add(mushee_subscribe)
subscribe_keyboard.add(register_wallet, airdrop_balance, referral, main_menu)
wallet_keyboard.add(change_wallet_address, main_menu)

@bot.message_handler(commands = ['start'])
@bot.message_handler(func=lambda message: message.text == '🏠 Home')
def send_welcome(message):
    try:
        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=no_custom_keyboard, parse_mode='html')
        # Get the user's unique ID
        user_id = message.chat.id
        # Check if the user was referred by someone
        if 'start=' not in message.text:        
            bot.reply_to(message, "👇 Forward a referrer's link ", reply_markup=no_custom_keyboard)
            
            if referred_link != {}:
                response = referred_link
                bot.send_message(message.chat.id, response, reply_markup=home_keyboard)
            elif referred_link == {}:                    
                @bot.message_handler(func=lambda message: message.chat.id == user_id and 'start=' in message.text)
                def handle_referrals(message):
                    # Extract the referrer's ID from the message
                    if referred_link == {}:                    
                            referred_link[user_id] = message.text
                            referrer_id = referred_link[user_id].split('start=')[1]
                    
                    # Add the referral data to the dictionary
                    referral_data[user_id] = {'referrer_id': referrer_id, 'referral_count': 0, 'referral_balance': 0}
                    
                    # Increment the referral count for the referrer
                    if referrer_id in referral_data:
                        referral_data[referrer_id]['referral_count'] += 1
                        
                        # Add the referral bonus to the referrer's balance
                        referral_data[referrer_id]['referral_balance'] += 10
                        
                    bot.reply_to(message, f"Welcome to our bot! You were referred by user ID {referrer_id}.", reply_markup=home_keyboard,)   
        else:
            # Add the user to the referral data dictionary with admin referrer
            referral_data[user_id] = {'referrer_id': None, 'referral_count': 0, 'referral_balance': 0,}
            bot.reply_to(message, f"Welcome to our bot! You were referred by NOBODY.", reply_markup=home_keyboard)
            
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        print(e)
        bot.reply_to(message, "An error has occurred")

@bot.message_handler(func=lambda message: message.text == '💢 Main Menu')
def send_commands(message):
    response = "Main Menu"
    bot.send_message(message.chat.id, response, reply_markup=main_menu_keyboard)

@bot.message_handler(func=lambda message: message.text == '🫡 Join us')
def subscribe_handler(message):
    try:
        # Get user ID
        user_id = message.chat.id
        # Check if user follows the group
        group_member= bot.get_chat_member('@funnychat4', user_id)
        if group_member.status != 'member':
            bot.reply_to(message, ERROR_MESSAGE, parse_mode='html')
            return

        # Check if the user follows the Twitter account
        # twitter_user = api.get_user('my_twitter_account')
        # twitter_follower = api.show_friendship(source_id=twitter_user.id_str, target_id=user_id)[0].following
        # if not twitter_follower:
        #     bot.reply_to(message, ERROR_MESSAGE)
        #     return
    
        bot.reply_to(message, SUCCESS_MESSAGE, reply_markup=subscribe_keyboard)
        wallet['airdrop_balance'] = user_airdrop
    except telebot.apihelper.ApiTelegramException as e:
        # Catch the ApiTelegramException and print the error message
        print(f"An error occurred: {e}")
        # Handle the error message appropriately
        bot.reply_to(message, ERROR_MESSAGE, parse_mode='html')

@bot.message_handler(func=lambda message: message.text == '📰 Change address')
def change_wallet_address(message):
    try:
        user_id = message.chat.id

        # Check if user already has a wallet then ask for wallet to be deleted
        if wallet:
            bot.reply_to(message, "🆕 What is your new address? ")
            
             # Wait for user input
            @bot.message_handler(func=lambda message: message.chat.id == user_id and '0x' in message.text)
            def handle_wallet_address(message):
                # Check if the message contains a BSC address
                match = re.search(BSC_ADDRESS_REGEX, message.text.strip())
                
                if match:
                    # Store the wallet address
                    bsc_address = match.group(0)
                    # Set wallet address to the wallet dictionary
                    wallet[user_id] = bsc_address
                    # Successful reply
                    bot.reply_to(message, "Your wallet address has been saved. Thank you!", reply_markup=subscribe_keyboard)
                else:
                    bot.reply_to(message, "Unacceptable wallet address.")
        else:
            bot.reply_to(message, "You don't have a wallet to reset.", reply_markup=subscribe_keyboard)
           
    except telebot.apihelper.ApiTelegramException as e:
        # Catch the ApiTelegramException and print the error message
        print(f"An error occurred: {e}")
        # Handle the error message appropriately
        bot.reply_to(message, "An error has occurred")

@bot.message_handler(func=lambda message: message.text == '😌 Wallet')
def prompt_for_wallet(message):
    try:
        user_id = message.chat.id
        
        # Check if user already has a wallet
        if user_id in wallet:
            bot.reply_to(message, "Your wallet address is {}.".format(wallet[user_id]), reply_markup=wallet_keyboard,)
        else:   
            # Ask the user for their BEP-20 wallet address
            bot.reply_to(message, WALLET_MESSAGE, parse_mode='html')
            
            # Wait for user input
            @bot.message_handler(func=lambda message: message.chat.id == user_id and '0x' in message.text)
            def handle_wallet_address(message):
                # Check if the message contains a BSC address
                match = re.search(BSC_ADDRESS_REGEX, message.text.strip())
                
                if match:
                    # Store the wallet address
                    bsc_address = match.group(0)
                    # Set wallet address to the wallet dictionary
                    wallet[user_id] = bsc_address
                    # Successful reply
                    bot.reply_to(message, "Your wallet address has been saved. Thank you!", reply_markup=subscribe_keyboard)
                else:
                    bot.reply_to(message, "Unacceptable wallet address.")
            
        
    except telebot.apihelper.ApiTelegramException as e:
        # Catch the ApiTelegramException and print the error message
        print(f"An error occurred: {e}")
        # Handle the error message appropriately
        bot.reply_to(message, "An error has ocurred")      
   
@bot.message_handler(func=lambda message: message.text == '🤑 Balance')
def check_airdrop_balance(message):
    # Get the user's unique ID
    user_id = message.chat.id
    
    # Calculate the total balance for the user
    total_balance = wallet.get('airdrop_balance', 0) + referral_data[user_id]['referral_balance']
    
    response = f"""
    😲 You've earned {wallet['airdrop_balance']} MSH from our airdrop\n\n🔄️ Your referral count is {referral_data[user_id]['referral_count']} and your referral balance is {referral_data[user_id]['referral_balance']} MSH.\n\n🗿 Total balance is {total_balance} MSH
    """
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == '🧑‍🤝‍🧑 Referrals')
def show_referral_info(message):
    # Get the user's unique ID
    user_id = message.chat.id
    
    # Check if the user has a referrer
    if referral_data[user_id]['referrer_id'] is not None:
        # Get the referrer's ID and balance
        referrer_id = referral_data[user_id]['referrer_id']
        
        # Send a message with the referral info
        bot.reply_to(message, f"You were referred by user ID {referrer_id}.\n\n Your referral count is {referral_data[user_id]['referral_count']} and your referral balance is {referral_data[user_id]['referral_balance']} MSH.\n\n🔗 Your referral link is https://t.me/{bot.get_me().username}?start={user_id}")
        
    else:
        # Send a message saying the user has no referrer
        bot.reply_to(message, f"😔 You were not referred by anyone. \n\n👉 Your referral count is {referral_data[user_id]['referral_count']} and your referral balance is {referral_data[user_id]['referral_balance']} MSH.\n\n🔗 Your referral link is https://t.me/{bot.get_me().username}?start={user_id}")

# @bot.message_handler(func=lambda message:True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
    
try:
    bot.infinity_polling()
except Exception as e:
    print(e)