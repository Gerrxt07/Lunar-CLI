import requests
from colorama import Fore, init
from replit import clear
import time
init(autoreset=True)

import psutil

import subprocess

import os
from dotenv import load_dotenv
load_dotenv()

import sqlite3
import bcrypt

import importlib

LunarVersion = 'V.1-Alpha-2'

# --- Search for missing Librarys | Try to install them if necessary

def init_missing_libraries():
    required = {
        'psutil': 'psutil',
        'Pillow': 'PIL',
        'python-dotenv': 'dotenv',
        'bcrypt': 'bcrypt',
        'replit': 'replit',
        'requests': 'requests',
        'colorama': 'colorama',
        'sqlite3': 'sqlite3',
        'time': 'time',
        'os': 'os',
    }

    missing = []

    for lib_name, import_name in required.items():

        try:
            importlib.import_module(import_name)

        except ImportError:

            print(Fore.RED + 'Missing: ' + lib_name)
            missing.append(lib_name)

    if missing:
        
        print(Fore.BLUE + 'Installing missing libraries...')

        for lib in missing:

            try:
                subprocess.check_call(['pip', 'install', lib])
                print(Fore.GREEN + lib + ' installed successfully.')

            except subprocess.CalledProcessError:

                print(Fore.RED + 'Problem with installing of ' + lib + '. Please install it manually:')
                exit(1)

    else:
        pass

init_missing_libraries()

# --- Search for new Updates on Github | Try to install it if necessary

def init_search_github():

    def get_latest_version():
        url = 'https://api.github.com/repos/Gerrxt07/Lunar-CLI/releases/latest'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['tag_name']
        return None

    latest_version = get_latest_version()

    if latest_version:

        if latest_version == LunarVersion:
            pass

        else:
            print(Fore.RED + 'New Update found: ' + latest_version + ' | Downloading...')
            # Download new Version
            # Install new Version
    else:

        print(Fore.YELLOW + 'Could not check for updates.')

#init_search_github()

# --- Initialize Database | Creating 'accounts' with 'id', 'username', 'password', 'permissions'

def init_db():

    with sqlite3.connect("main.db") as db_connection:

        cursor = db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, permissions TEXT DEFAULT 'user')")
        db_connection.commit()

init_db()

def create_account(username, password):
    def check_username_exists(username):
        with sqlite3.connect("main.db") as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
            return cursor.fetchone() is not None
    
    if check_username_exists(username):
        print(Fore.RED + 'Username already exists.')
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    with sqlite3.connect("main.db") as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO accounts (username, password, permissions) VALUES (?, ?, 'user')", (username, hashed_password))
        db_connection.commit()
        print(Fore.GREEN + 'User created successfully.')

def check_admin_exists():
    with sqlite3.connect("main.db") as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE permissions = 'admin'")
        return cursor.fetchone() is not None

def is_secure(username, password):
    if len(username) < 3 or len(password) < 8:
        return False
    if username.lower() == "admin" or password.lower() in ["password", "12345678", "admin", "qwerty", "abcd1234"]:
        return False
    return True

def create_admin_account():
    while True:
        print(Fore.RED + "It's your first start of Lunar. Please create an admin account.")
        print('')
        admin_username = input(Fore.CYAN + "Admin Username: ").strip()
        print('')
        admin_password = input(Fore.CYAN + "Admin Password: ").strip()

        if admin_username and admin_password:
            if is_secure(admin_username, admin_password):
                hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
                with sqlite3.connect("main.db") as db_connection:
                    cursor = db_connection.cursor()
                    cursor.execute("INSERT INTO accounts (username, password, permissions) VALUES (?, ?, 'admin')", (admin_username, hashed_password))
                    db_connection.commit()
                    print('')
                    print(Fore.GREEN + 'Admin account created successfully. Please restart Lunar-CLI!')
                    print('')
                    time.sleep(30)
                    exit()
            else:
                print('')
                print(Fore.RED + "Username or password is too weak. Please try again.")
                print('')
        else:
            print('')
            print(Fore.RED + "Both username and password are required. Please try again.")
            print('')

def login(username, password):
    with sqlite3.connect("main.db") as db_connection:

        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return user
        
    return None

def list_users(logged_in_user):
    with sqlite3.connect("main.db") as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT username FROM accounts")
        users = cursor.fetchall()
        for user in users:
            user_name = user[0]
            if user_name == logged_in_user:
                print(Fore.GREEN + f"{user_name} (YOU)")
            else:
                print(Fore.CYAN + user_name)

def debug_admin_rights(logged_in_admin):
    if logged_in_admin:
        print(Fore.GREEN + "You have admin rights.")
    else:
        print(Fore.RED + "You do not have admin rights.")

# -------------------------------------------------------------------------------------------------------

def main():
    def logo():
        clear()
        print('')
        print(Fore.CYAN + '┌───────────────────────────────────────────────────┐')
        print(Fore.CYAN + '│ _    _   _ _   _    _    ____      ____ _     ___ │')
        print(Fore.CYAN + '│| |  | | | | \\ | |  / \\  |  _ \\    / ___| |   |_ _|│')
        print(Fore.CYAN + '│| |  | | | |  \\| | / _ \\ | |_) |  | |   | |    | | │')
        print(Fore.CYAN + '│| |__| |_| | |\\  |/ ___ \\|  _ <   | |___| |___ | | │')
        print(Fore.CYAN + '│|_____\\___/|_| \\_/_/   \\_\\_| \\_\\   \\____|_____|___|│')
        print(Fore.CYAN + '└───────────────────────────────────────────────────┘')
        print('')
        print(Fore.CYAN + 'Lunar CLI | Version: ' + LunarVersion)
        print('')
        print(Fore.CYAN + '  ─────────────────────────────────────────────────')
        print('')

    logo()

    if not check_admin_exists():
        create_admin_account()

    logged_in = False
    logged_in_admin = False
    logged_in_user = 'Anonymous'

    print(Fore.CYAN + 'Type "help" for help.')

    while True:
        print('')
        console_input = input(Fore.CYAN + logged_in_user + '@LunarCLI: ').strip()
        print('')

        if console_input == 'exit':
            print(Fore.CYAN + 'Exiting Lunar...')
            time.sleep(2)
            exit()

        elif console_input == 'help':
            print(Fore.CYAN + 'Available commands:')
            print(Fore.CYAN + ' - user | Manage users')
            print(Fore.CYAN + ' - info | Show engine informations')
            print(Fore.CYAN + ' - exit | Exit Lunar')
            print(Fore.CYAN + ' - clear | Clear the terminal')

        elif console_input == 'debug':
            debug_admin_rights(logged_in_admin)
            
        elif console_input == 'clear':
            clear()
            
        elif console_input == 'info':
            print(Fore.CYAN + 'You are using: Lunar ' + LunarVersion)
            print(Fore.CYAN + 'Created by Gerrxt from Lunar')

        elif console_input.startswith('user'):
            parts = console_input.split()

            if len(parts) == 1:
                print(Fore.CYAN + 'Please use "user help" for more information.')

            elif parts[1] == 'help':
                print(Fore.CYAN + 'Available "user" commands:')
                print(Fore.CYAN + '  - user create <username> <password>  - Create a new user.')
                print(Fore.CYAN + '  - user login <username> <password>   - Login as an existing user.')
                print(Fore.CYAN + '  - user list - List all users.')
                print(Fore.CYAN + '  - user logout - Logout from your account.')

            elif parts[1] == 'logout':
                if logged_in:
                    logged_in = False
                    logged_in_user = 'Anonymous'
                    logged_in_admin = False
                    print(Fore.GREEN + 'Logged out successfully.')
                else:
                   print(Fore.RED + "You are not logged in.")
            
            elif parts[1] == 'list':
                if logged_in:
                    list_users(logged_in_user)
                else:
                   print(Fore.RED + "You need to be logged in to use this command.")

            elif parts[1] == 'create':
                if len(parts) == 3:
                    print(Fore.CYAN + 'You need to type in a username and a password.')
                elif len(parts) == 4:
                    _, _, username, password = parts
                    create_account(username, password)
                else:
                    print(Fore.CYAN + 'To create a user, type: user create <username> <password>')

            elif parts[1] == 'login':
                if len(parts) == 3:
                    print(Fore.CYAN + 'You need to type in a username and a password.')
                elif len(parts) == 4:
                    _, _, username, password = parts
                    user = login(username, password)
                    if user:
                        logged_in = True
                        logged_in_user = user[1]
                        logged_in_admin = user[3] == 'admin'
                        print(Fore.GREEN + f'Logged in as {logged_in_user}.')
                    else:
                        print(Fore.RED + 'Invalid username or password.')
                else:
                    print(Fore.CYAN + 'To login, type: user login <username> <password>')

        else:
            print(Fore.CYAN + 'Unknown command. Type "help" for help.')

main()