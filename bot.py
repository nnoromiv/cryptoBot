import os
import telebot
import re
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instance of the robot
BOTTOKEN = os.environ['BOTTOKEN']
bot = telebot.TeleBot(BOTTOKEN)

try:
    # Create a connection
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )

    # instantiate a connection to the database
    cursor = connection.cursor()

    # execute a query to get a list of all databases
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    # iterate over the list of databases and check if the specified database exists
    database_name = "mushee_bot"
    for db in cursor:
        if db[0] == database_name:
            cursor.execute("USE mushee_bot;")
            break
        else:
            cursor.execute("CREATE DATABASE mushee_bot; USE mushee_bot;")

    # Create the referral_link table
    check_for_referral_link_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'mushee_bot' AND table_name = 'referral_link';"""
    referral_link_table_creation_query = """CREATE TABLE referral_link (
            user_id INT PRIMARY KEY,
            referred_link VARCHAR(255)
        );"""
    select_referral_link_query = """SELECT * FROM referral_link"""

    cursor.execute(check_for_referral_link_table)
    referral_link_count = cursor.fetchone()[0]
    if referral_link_count == 0:
        cursor.execute(referral_link_table_creation_query)
    elif referral_link_count == 1:
        cursor.execute(select_referral_link_query)
    else:
        print('Referral link table cannot be found')

    cursor.fetchall()  # read the result of the last query   

    # Create the referral_data table
    check_for_referral_data_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'mushee_bot' AND table_name = 'referral_data';"""
    referral_data_table_creation_query = """CREATE TABLE referral_data (
            user_id VARCHAR(255) PRIMARY KEY,
            referrer_id VARCHAR(255),
            referral_count INT,
            referral_balance DECIMAL(18,8)
        );"""
    select_referral_data_query = """SELECT * FROM referral_data"""

    cursor.execute(check_for_referral_data_table)
    referral_data_count = cursor.fetchone()[0]
    if referral_data_count == 0:
        cursor.execute(referral_data_table_creation_query)
    elif referral_data_count == 1:
        cursor.execute(select_referral_data_query)
    else:
        print('Referral data table cannot be found')

    cursor.fetchall()  # read the result of the last query   


    # Create the wallet table
    check_for_wallet_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'mushee_bot' AND table_name = 'wallet';"""
    wallet_table_creation_query = """CREATE TABLE wallet (
            user_id BIGINT PRIMARY KEY,
            address VARCHAR(42) NOT NULL,
            balance INT
        );"""
    select_wallet_query = """SELECT * FROM wallet"""
        
    cursor.execute(check_for_wallet_table)
    wallet_count = cursor.fetchone()[0]
    if wallet_count == 0:
        cursor.execute(wallet_table_creation_query)
    elif wallet_count == 1:
        cursor.execute(select_wallet_query)
    else:
        print('Wallet table cannot be found')
        
        
    cursor.fetchall()  # read the result of the last query   
    cursor.close()

    # close the connection
    connection.close()
except Error as e:
    print(f"Error encountered is: {e}")

# Initializations
user_airdrop = 50
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
affiliate = telebot.types.KeyboardButton('➕ Affiliate')

no_custom_keyboard = telebot.types.ReplyKeyboardRemove()
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
home_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
subscribe_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
wallet_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
affiliate_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
set_wallet_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)


main_menu_keyboard.add(register_wallet, airdrop_balance, referral, change_wallet_address)
set_wallet_keyboard.add(register_wallet)
home_keyboard.add(mushee_subscribe)
subscribe_keyboard.add(register_wallet, airdrop_balance, referral, main_menu)
wallet_keyboard.add(change_wallet_address, main_menu)
affiliate_keyboard.add(affiliate)

# Check if user_id exist in the table
def referral_link_exists(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT COUNT(*) FROM referral_link WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    count = cursor.fetchone()[0]
    return count > 0
# Collect the referral link using the user_id
def user_referral_link(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT referred_link FROM referral_link WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    referred_link = cursor.fetchone()[0]
    return referred_link
# Store the referral link
def insert_referral_link(user_id, referred_link):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    insert_query = "INSERT INTO referral_link (user_id, referred_link) VALUES (%s, %s)"
    values = (user_id, referred_link)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
# Populate the referral data
def populate_referral_data(user_id, referrer_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    insert_query = "INSERT INTO referral_data (user_id, referrer_id, referral_count, referral_balance) VALUES (%s, %s, %s, %s)"
    values = (user_id, referrer_id, 0, 0)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
# Get referral data of user
def referral_user_data():
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT referrer_id FROM referral_data LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(select_query)
    users = cursor.fetchall()
    referral_datas = [referral_data[0] for referral_data in users]
    return referral_datas
# Get referrer data from a user
def referrer_data(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT referrer_id FROM referral_data WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    referrer_data = cursor.fetchone()[0]
    return referrer_data
# Get referrer count
def referral_user_count(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT referral_count FROM referral_data WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    count = cursor.fetchone()[0]
    return count
# Get referrer balance
def referral_user_balance(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT referral_balance FROM referral_data WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    balance = cursor.fetchone()[0]
    return balance
# Update the referrer count of a user
def increment_referral_count(user_id, referral_count):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    update_query = "UPDATE referral_data SET referral_count = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (referral_count, user_id,))
    connection.commit()
# Update the referrer balance of a user
def increment_referral_balance(user_id, referral_balance):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    update_query = "UPDATE referral_data SET referral_balance = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (referral_balance, user_id,))
    connection.commit()

def insert_wallet_data(user_id, address):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    insert_query = "INSERT INTO wallet (user_id, address) VALUES (%s, %s)"
    values = (user_id, address)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()

def select_wallet():
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT user_id FROM wallet LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(select_query)
    users = cursor.fetchall()
    user_ids = [userid[0] for userid in users]    
    return user_ids
    
def select_wallet_by_user_id(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT address FROM wallet WHERE user_id = %s LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    wallet_address = cursor.fetchone()[0]
    return wallet_address

def insert_wallet_address(user_id, address):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    insert_query = "INSERT INTO wallet (user_id, address, balance) VALUES (%s, %s, %s)"
    values = (user_id, address, 0)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
    
def select_balance_by_user_id(user_id):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    select_query = "SELECT balance FROM wallet WHERE user_id = %s LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(select_query, (user_id,))
    wallet_balance = cursor.fetchone()[0]
    return wallet_balance

def update_wallet_balance(user_id, balance):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    update_query = "UPDATE wallet SET balance = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (balance, user_id,))
    connection.commit()

def update_wallet_address(user_id, address):
    connection = mysql.connector.connect(
        host='localhost',
        database='mushee_bot',
        user='root',
        password=''
    )
    update_query = "UPDATE wallet SET address = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (address, user_id,))
    connection.commit()
    
@bot.message_handler(commands = ['start'])
@bot.message_handler(func=lambda message: message.text == '🏠 Home')
def send_welcome(message):
    try:
        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=home_keyboard, parse_mode='html')        
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        print(e)
        bot.reply_to(message, f"An error has occurred: {e}")

@bot.message_handler(func=lambda message: message.text == '➕ Affiliate')
def handle_referrals(message):
    try:
        # Get the user's unique ID
        user_id = message.chat.id
        # Check if the user was referred by someone
        if 'start=' not in message.text:        
            bot.reply_to(message, "👇 Forward a referrer's link ", reply_markup=no_custom_keyboard)
            
            if referral_link_exists(user_id) is True:
                response = user_referral_link(user_id)
                bot.send_message(message.chat.id, response, reply_markup=set_wallet_keyboard)
            elif referral_link_exists(user_id) is False:                   
                @bot.message_handler(func=lambda message: message.chat.id == user_id and 'start=' in message.text)
                def handle_referrals(message):
                    # Extract the referrer's ID from the message
                    if referral_link_exists(user_id) is False:      
                            insert_referral_link(user_id, message.text)             
                            referrer = message.text.split('start=')[1]
                    
                    # Add the referral data to the dictionary
                    populate_referral_data(user_id, referrer)
                    referral_user_data()
                    
                    for data in referral_user_data():                                        
                        # Increment the referral count for the referrer
                        if data == referrer:
                            new_count = referral_user_count(data)+ 1
                            increment_referral_count(data, new_count)
                                    
                            # Add the referral bonus to the referrer's balance
                            new_balance = referral_user_balance(data) + 10
                            increment_referral_balance(data, new_balance)              
                        
                    bot.reply_to(message, f"Welcome to our bot! You were referred by user ID {data}.", reply_markup=set_wallet_keyboard,)
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        print(e)
        bot.reply_to(message, f"An error has occurred: {e}")
        
@bot.message_handler(func=lambda message: message.text == '💢 Main Menu')
def send_commands(message):
    response = "💢 Main Menu"
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
    
        bot.reply_to(message, SUCCESS_MESSAGE, reply_markup=affiliate_keyboard)
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
        if user_id in select_wallet():
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
                    update_wallet_address(user_id, bsc_address)
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
        if user_id in select_wallet():
            bot.reply_to(message, f"Your wallet address is {select_wallet_by_user_id(user_id)}", reply_markup=wallet_keyboard,)
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
                    
                    insert_wallet_address(user_id, bsc_address)
                    # Successful reply
                    bot.reply_to(message, "Your wallet address has been saved. Thank you!", reply_markup=subscribe_keyboard)
                    update_wallet_balance(user_id, user_airdrop)
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
    total_balance = select_balance_by_user_id(user_id) + referral_user_balance(user_id)
    
    response = f"""
    😲 You've earned {select_balance_by_user_id(user_id)} MSH from our airdrop\n\n🔄️ Your referral count is {referral_user_count(user_id)} and your referral balance is {referral_user_balance(user_id)} MSH.\n\n🗿 Total balance is {total_balance} MSH
    """
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == '🧑‍🤝‍🧑 Referrals')
def show_referral_info(message):
    # Get the user's unique ID
    user_id = message.chat.id
        
    bot.reply_to(message, f"You were referred by user ID {referrer_data(user_id)}.\n\n Your referral count is {referral_user_count(user_id)} and your referral balance is {int(referral_user_balance(user_id))} MSH.\n\n🔗 Your referral link is https://t.me/{bot.get_me().username}?start={user_id}")

# @bot.message_handler(func=lambda message:True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
    
try:
    bot.infinity_polling()
except Exception as e:
    print(f"Error ocurred: {e}")