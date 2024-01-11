# The above code is importing the "os" module in Python. This module provides a way of using operating
# system dependent functionality like reading or writing to the file system.
import os
# The above code is importing the `telebot` module in Python. This module is used to create a Telegram
# bot and interact with the Telegram API. However, the code snippet is incomplete and does not contain
# any further instructions or code to create a bot or perform any actions.
import telebot
# The above code is importing the regular expression module "re" in Python.
import re
# The above code is importing the `mysql.connector` module in Python. This module provides a way to
# connect to a MySQL database and perform various operations such as executing queries, inserting
# data, updating data, and deleting data.
import mysql.connector
# The above code is importing the `Error` class from the `mysql.connector` module in Python. This
# class is typically used to handle errors that may occur when working with a MySQL database using the
# `mysql.connector` module.
from mysql.connector import Error
# The above code is importing the `load_dotenv` function from the `dotenv` module. This function is
# used to load environment variables from a `.env` file into the current environment.
from dotenv import load_dotenv
# Load environment variables from .env file
# The above code is loading environment variables from a .env file into the current environment using
# the `load_dotenv()` function from the `dotenv` library in Python. This is useful for keeping
# sensitive information, such as API keys or database credentials, separate from the code and stored
# securely in a file.
load_dotenv()
# Instance of the robot
# The above code is initializing a Telegram bot using the `telebot` library in Python. It is
# retrieving the bot token from an environment variable named `BOTTOKEN` using the `os` library and
# then passing it to the `TeleBot` constructor to create a new instance of the bot.
BOTTOKEN = os.environ['BOTTOKEN']
bot = telebot.TeleBot(BOTTOKEN)
# The above code is creating and/or checking for the existence of three tables in a MySQL database:
# referral_link, referral_data, and wallet. It first establishes a connection to the database, then
# checks if the specified database exists and creates it if it doesn't. It then checks for the
# existence of each table and creates them if they don't exist. Finally, it closes the connection to
# the database.
RAILWAY_HOST = os.environ['RAILWAY_HOST']
RAILWAY_DB = os.environ['RAILWAY_DB']
RAILWAY_USER = os.environ['RAILWAY_USER']
RAILWAY_PASSWORD = os.environ['RAILWAY_PASSWORD']
RAILWAY_PORT = os.environ['RAILWAY_PORT']
try:
    # Create a connection
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    # instantiate a connection to the database
    cursor = connection.cursor()
    # execute a query to get a list of all databases
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    # iterate over the list of databases and check if the specified database exists
    database_name = "railway"
    for db in cursor:
        if db[0] == database_name:
            cursor.execute("USE railway;")
            break
        else:
            cursor.execute("CREATE DATABASE railway; USE railway;")
    # Create the referral_link table
    check_for_referral_link_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'railway' AND table_name = 'referral_link';"""
    referral_link_table_creation_query = """CREATE TABLE referral_link (
            user_id INT PRIMARY KEY,
            referred_link VARCHAR(100)
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
    check_for_referral_data_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'railway' AND table_name = 'referral_data';"""
    referral_data_table_creation_query = """CREATE TABLE referral_data (
            user_id VARCHAR(100) PRIMARY KEY,
            referrer_id VARCHAR(100),
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
    check_for_wallet_table = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'railway' AND table_name = 'wallet';"""
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
👏 Follow <b><a href="https://twitter.com/nnoromiv">Crypto Twitter</a></b>

👏 Join <b><a href="https://t.me/nnoromiv">Crypto Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/nnoromiv">Crypto Telegram Group</a></b>

😒 Connect with us to continue
"""
WALLET_MESSAGE = f"""
🗒️ What is your BEP-20(BSC) wallet address!!?

<b><i> Please submit your Trustwallet or SafePal address. Address must be from a Decentralized  platform</i></b>
"""
WELCOME_MESSAGE = f"""
👋 Hello, Old sport! 

🌞 1 tPNA = $0.3
⛅ Get <b>50 tPNA</b> for joining and completing task
🌬️ Get <b>5 tPNA</b> per referral 

📝 Airdrop will end soon...

🔥 Complete the task and be deemed eligible

🗒️ <b>TASK:</b>

👏 Follow <b><a href="https://twitter.com/nnoromiv">Crypto Twitter</a></b>

👏 Join <b><a href="https://t.me/nnoromiv">Crypto Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/nnoromiv">Crypto Telegram Group</a></b>

🧏 Use only positive words to chat in the group otherwise you will miss the big opportunity

<b>NOTE: All tasks are mandatory</b>

<b>You can use Admin referral Link: https://t.me/{bot.get_me().username}?start={1121070064} </b>
"""
# Define the regular expression to match BSC addresses
# The above code is defining a regular expression pattern using the `re` module in Python. The pattern
# is used to match a string that represents a Binance Smart Chain (BSC) address.
BSC_ADDRESS_REGEX = r'^0x([A-Fa-f0-9]{40})$'
# Custom define keyboard
# The above code is defining keyboard buttons for a Telegram bot using the telebot library in Python.
# The buttons include options for navigating to the home or main menu, subscribing to a service,
# registering a wallet, changing a wallet address, checking airdrop balance, viewing referrals, and
# accessing an affiliate program.
home_button = telebot.types.KeyboardButton('🏠 Home')
main_menu = telebot.types.KeyboardButton('💢 Main Menu')
crypto_subscribe = telebot.types.KeyboardButton('🫡 Join us')
register_wallet = telebot.types.KeyboardButton('😌 Wallet')
change_wallet_address = telebot.types.KeyboardButton('📰 Change address')
airdrop_balance = telebot.types.KeyboardButton('🤑 Balance')
referral = telebot.types.KeyboardButton('🧑‍🤝‍🧑 Referrals')
affiliate = telebot.types.KeyboardButton('➕ Affiliate')
# The above code is creating several instances of the `ReplyKeyboardMarkup` and `ReplyKeyboardRemove`
# classes from the `telebot.types` module in Python. These instances are used to create custom
# keyboards with different options for the user to choose from in a Telegram bot. The
# `resize_keyboard` parameter is set to `True` for all instances, which means that the keyboard will
# be resized to fit the user's screen. The `no_custom_keyboard` instance is used to remove any custom
# keyboard that was previously displayed to the user. The other instances are used to display
# different options to the user,
no_custom_keyboard = telebot.types.ReplyKeyboardRemove()
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
home_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
subscribe_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
wallet_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
affiliate_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
set_wallet_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# The above code is defining and adding different buttons to various keyboard menus in a Python
# program. Specifically, it is adding buttons for options such as registering a wallet, checking
# airdrop balance, accessing referral information, changing wallet address, subscribing to a service,
# and accessing affiliate information. These buttons are added to different keyboard menus such as the
# main menu, set wallet menu, home menu, subscribe menu, wallet menu, and affiliate menu.
main_menu_keyboard.add(register_wallet, airdrop_balance, referral, change_wallet_address)
set_wallet_keyboard.add(register_wallet)
home_keyboard.add(crypto_subscribe)
subscribe_keyboard.add(register_wallet, airdrop_balance, referral, main_menu)
wallet_keyboard.add(change_wallet_address, main_menu)
affiliate_keyboard.add(affiliate)

def execute_query(query, params=None):
    """
    Executes the given SQL query on the MySQL database.
    
    :param query: The SQL query to execute.
    :param params: Optional parameter that contains any variables that are used in the SQL query.
    :return: The result of the query, as returned by the MySQL database.
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return result

def referral_link_exists(user_id):
    """
    Checks if a referral link exists for a given user ID in the MySQL database.
    
    :param user_id: The user ID to check.
    :return: True if a referral link exists, False otherwise.
    """
    select_query = "SELECT COUNT(*) FROM referral_link WHERE user_id = %s"
    count = execute_query(select_query, (user_id,))
    return count > 0

def user_referral_link(user_id):
    """
    The function retrieves a referred link from a MySQL database based on a user ID.
    
    :param user_id: The user ID is a unique identifier for a specific user in the system. It is used to
    retrieve the referral link associated with that user from the database
    :return: the referred link associated with the user ID passed as a parameter.
    """
    select_query = "SELECT referred_link FROM referral_link WHERE user_id = %s"
    referred_link = execute_query(select_query, (user_id,))
    return referred_link

def insert_referral_link(user_id, referred_link):
    """
    This function inserts a user's referral link into a MySQL database.
    
    :param user_id: The ID of the user who is being referred
    :param referred_link: The referral link that the user has shared with someone else. It could be a
    unique URL or code that identifies the user as the referrer
    """
    with mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    ) as connection:
        insert_query = "INSERT INTO referral_link (user_id, referred_link) VALUES (%s, %s)"
        values = (user_id, referred_link)
        with connection.cursor() as cursor:
            cursor.execute(insert_query, values)
        connection.commit()

def populate_referral_data(user_id, referrer_id):
    """
    This function populates referral data for a user with their user ID and referrer ID.
    
    :param user_id: The ID of the user for whom referral data is being populated
    :param referrer_id: The ID of the user who referred the new user
    """
    with mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    ) as connection:
        insert_query = "INSERT INTO referral_data (user_id, referrer_id, referral_count, referral_balance) VALUES (%s, %s, %s, %s)"
        values = (user_id, referrer_id, 0, 0)
        with connection.cursor() as cursor:
            cursor.execute(insert_query, values)
        connection.commit()

def referral_user_data():
    """
    This function retrieves the referrer IDs from the "referral_data" table in the "crypto_bot"
    database.
    :return: a list of referrer IDs from the "referral_data" table in the "crypto_bot" database.
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    select_query = "SELECT referrer_id FROM referral_data"
    cursor = connection.cursor()
    cursor.execute(select_query)
    referral_datas = [referral_data[0] for referral_data in cursor]
    return referral_datas

def referrer_data(user_id):
    """
    The function retrieves the referrer ID for a given user ID from a MySQL database.
    
    :param user_id: The user ID is a parameter that is passed to the function. It is used to retrieve
    the referrer ID from the database for the given user. The referrer ID is the ID of the user who
    referred the current user to the platform or service
    :return: the referrer_id of a user from the referral_data table in the crypto_bot database, based on
    the user_id provided as an argument.
    """
    select_query = "SELECT referrer_id FROM referral_data WHERE user_id = %s"
    referrer_data = execute_query(select_query, (user_id,))
    return referrer_data
def referral_user_count(user_id):
    """
    The function retrieves the referral count for a given user ID from a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
    It is used to retrieve the referral count for that particular user
    :return: the referral count of a user with the given user_id from the referral_data table in the
    crypto_bot database.
    """
    select_query = "SELECT referral_count FROM referral_data WHERE user_id = %s"
    count = execute_query(select_query, (user_id,))
    return count
def referral_user_balance(user_id):
    """
    The function retrieves the referral balance of a user from a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
    This function retrieves the referral_balance for the user with the given user_id
    :return: the referral balance of a user with the given user_id.
    """
    select_query = "SELECT referral_balance FROM referral_data WHERE user_id = %s"
    balance = execute_query(select_query, (user_id,))
    return balance
def increment_referral_count(user_id, referral_count):
    """
    This function updates the referral count of a user in a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
    It is used to identify which user's referral count needs to be updated
    :param referral_count: The number of referrals that the user has made
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    update_query = "UPDATE referral_data SET referral_count = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (referral_count, user_id,))
    connection.commit()
def increment_referral_balance(user_id, referral_balance):
    """
    This function updates the referral balance of a user in a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the referral_data table.
    It is used to identify which user's referral balance needs to be updated
    :param referral_balance: The amount by which the referral balance needs to be incremented for the
    given user ID
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    update_query = "UPDATE referral_data SET referral_balance = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (referral_balance, user_id,))
    connection.commit()
def insert_wallet_data(user_id, address):
    """
    This function inserts user wallet data (user ID and address) into a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a user in the system. It is used to associate
    wallet data with a specific user
    :param address: The address parameter is a string that represents the wallet address of a user. It
    is used as a value to be inserted into the "address" column of the "wallet" table in a MySQL
    database
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    insert_query = "INSERT INTO wallet (user_id, address) VALUES (%s, %s)"
    values = (user_id, address)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
def select_wallet():
    """
    The function selects the user IDs from the "wallet" table in the "crypto_bot" database and returns
    them as a list.
    :return: a list of user IDs from the "wallet" table in the "crypto_bot" database.
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    select_query = "SELECT user_id FROM wallet LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(select_query)
    users = cursor.fetchall()
    user_ids = [userid[0] for userid in users]    
    return user_ids
def select_wallet_by_user_id(user_id):
    """
    This function selects the wallet address associated with a given user ID from a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a user in the database. This function selects
    the wallet address associated with the given user ID from the "wallet" table in the "crypto_bot"
    database
    :return: the wallet address of the user with the given user_id from the "wallet" table in the
    "crypto_bot" database.
    """
    select_query = "SELECT address FROM wallet WHERE user_id = %s LIMIT 1"
    wallet_address = execute_query(select_query, (user_id,))
    return wallet_address
def insert_wallet_address(user_id, address):
    """
    The function inserts a user's wallet address and sets their balance to 0 in a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a user in the system. It could be a numerical
    or alphanumeric value that is assigned to each user when they register or create an account
    :param address: The wallet address that the user wants to insert into the database
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    insert_query = "INSERT INTO wallet (user_id, address, balance) VALUES (%s, %s, %s)"
    values = (user_id, address, 0)
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
def select_balance_by_user_id(user_id):
    """
    This function selects the balance of a user's wallet from a MySQL database based on their user ID.
    
    :param user_id: The user ID is a unique identifier for a user in the database. It is used to
    retrieve the wallet balance associated with that user
    :return: the balance of a user's wallet from the database, based on their user ID.
    """
    select_query = "SELECT balance FROM wallet WHERE user_id = %s LIMIT 1"
    wallet_balance = execute_query(select_query, (user_id,))
    return wallet_balance
def update_wallet_balance(user_id, balance):
    """
    The function updates the balance of a user's wallet in a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the database. It is used
    to identify which user's wallet balance needs to be updated
    :param balance: The new balance that you want to update for the user's wallet
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    update_query = "UPDATE wallet SET balance = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (balance, user_id,))
    connection.commit()
def update_wallet_address(user_id, address):
    """
    The function updates the wallet address of a user in a MySQL database.
    
    :param user_id: The user ID is a unique identifier for a specific user in the database. It is used
    to identify which user's wallet address needs to be updated
    :param address: The new wallet address that needs to be updated in the database
    """
    connection = mysql.connector.connect(
        host=RAILWAY_HOST,
        database=RAILWAY_DB,
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        port=RAILWAY_PORT
    )
    update_query = "UPDATE wallet SET address = %s WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (address, user_id,))
    connection.commit()
# The above code is defining two message handlers for a Python Telegram bot. The first handler is
# triggered when the user sends the "/start" command to the bot, and the second handler is triggered
# when the user sends the "🏠 Home" message to the bot. Both handlers will execute a specific block of
# code when triggered.
@bot.message_handler(commands = ['start'])
@bot.message_handler(func=lambda message: message.text == '🏠 Home')
def send_welcome(message):
    """
    This function sends a welcome message to a user and handles any errors that may occur.
    
    :param message: The message object that the bot received from the user. It contains information
    about the user who sent the message, the chat where the message was sent, and the text of the
    message
    """
    try:
        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=home_keyboard, parse_mode='html')        
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the error message appropriately
        bot.reply_to(message, f"An error has occurred: {e}")
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using a lambda function to check if the user's message text is equal
# to "➕ Affiliate". If the message matches, the handler will be triggered and the bot will perform
# some action.
@bot.message_handler(func=lambda message: message.text == '➕ Affiliate')
def handle_referrals(message):
    """
    This function handles referrals for a Telegram bot by checking if a user was referred by someone and
    adding referral data to a dictionary.
    
    :param message: The message object received by the bot from the user. It contains information about
    the user, the chat, and the message itself
    """
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
                @bot.message_handler(func=lambda message: message.chat.id == user_id and 'https://t.me/cryptoBot?start=' in message.text)
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
        bot.reply_to(message, f"An error has occurred") 
# The above code is defining a message handler for the bot. It will handle messages that have the text
# "💢 Main Menu". When a user sends a message with this text, the function associated with this
# handler will be executed.
@bot.message_handler(func=lambda message: message.text == '💢 Main Menu')
def send_commands(message):
    """
    This function sends a main menu message with a keyboard as a response to a user's message.
    
    :param message: The message object that contains information about the incoming message, such as the
    chat ID, sender ID, and message text
    """
    response = "💢 Main Menu"
    bot.send_message(message.chat.id, response, reply_markup=main_menu_keyboard)

# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the incoming message text is
# equal to "🫡 Join us". If the message text matches, the handler will be triggered and the bot will
# perform some action.
@bot.message_handler(func=lambda message: message.text == '🫡 Join us')
def subscribe_handler(message):
    """
    This function checks if a user is a member of a Telegram group and if they follow a Twitter account,
    and replies with a success message and a keyboard if they meet the requirements, or an error message
    if they don't.
    
    :param message: The message object that triggered the handler function. It contains information
    about the message, such as the chat it was sent in, the sender, and the text of the message
    :return: The function does not return anything, it only sends a reply message to the user or catches
    an exception and sends an error message.
    """
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

# The above code is defining a message handler for a Telegram bot using the Python programming
# language. The handler is triggered when the user sends a message with the text "📰 Change address".
@bot.message_handler(func=lambda message: message.text == '📰 Change address')
def change_wallet_address(message):
    """
    This function allows a user to change their wallet address by prompting them for a new address and
    verifying that it is a valid BSC address.
    
    :param message: The message object that contains information about the user's input and the chat
    they are in
    """
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
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "😌 Wallet". If the message matches, the handler will be triggered and the bot will perform
# some action.
@bot.message_handler(func=lambda message: message.text == '😌 Wallet')
def prompt_for_wallet(message):
    """
    This function prompts the user to input their BEP-20 wallet address, checks if it is valid, and
    stores it in the database if it is.
    
    :param message: The message object received by the bot. It contains information about the message
    sent by the user, such as the text, chat ID, and user ID
    """
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
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "🤑 Balance". If the message matches, the handler will be triggered and the bot will
# perform some action (which is not shown in the code snippet).
@bot.message_handler(func=lambda message: message.text == '🤑 Balance')
def check_airdrop_balance(message):
    """
    The function calculates the total balance of a user's airdrop and referral earnings and sends a
    message with the details.
    
    :param message: The message object that contains information about the user who sent the message and
    the content of the message
    """
    # Get the user's unique ID
    user_id = message.chat.id
    
    # Calculate the total balance for the user
    total_balance = select_balance_by_user_id(user_id) + referral_user_balance(user_id)
    
    response = f"""
    😲 You've earned {select_balance_by_user_id(user_id)} tPNA from our airdrop\n\n🔄️ Your referral count is {referral_user_count(user_id)} and your referral balance is {referral_user_balance(user_id)} tPNA.\n\n🗿 Total balance is {total_balance} tPNA
    """
    bot.send_message(message.chat.id, response)
# The above code is defining a message handler for a Telegram bot using the Python programming
# language. Specifically, it is using the `func` parameter to check if the user's message text is
# equal to "🧑‍🤝‍🧑 Referrals". If the user sends this message, the message handler will be triggered
# and the bot will perform some action (which is not shown in the code snippet).
@bot.message_handler(func=lambda message: message.text == '🧑‍🤝‍🧑 Referrals')
def show_referral_info(message):
    """
    The function displays referral information for a user, including their referrer's ID, referral
    count, referral balance, and referral link.
    
    :param message: The message object that contains information about the user who triggered the
    function
    """
    # Get the user's unique ID
    user_id = message.chat.id
        
    bot.reply_to(message, f"You were referred by user ID {referrer_data(user_id)}.\n\n Your referral count is {referral_user_count(user_id)} and your referral balance is {int(referral_user_balance(user_id))} tPNA.\n\n🔗 Your referral link is https://t.me/{bot.get_me().username}?start={user_id}") 
# The above code is using the Python library `python-telegram-bot` to create a bot that can receive
# and respond to messages on the Telegram messaging platform. The `bot.infinity_polling()` method is
# used to continuously poll for new messages and handle them appropriately. The `try-except` block is
# used to catch any exceptions that may occur during the execution of the `infinity_polling()` method
# and print an error message with the details of the exception.
try:
    bot.infinity_polling()
except Exception as e:
    print(f"Error ocurred: {e}")