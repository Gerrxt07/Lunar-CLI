# Nach fehlending Libs suchen -> pip install -r requirements.txt

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

LunarVersion = 'V.1'

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
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, permissions TEXT DEFAULT 'user')")
        db_connection.commit()

init_db()

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

    logo()

    time.sleep(1)
    logged_in = False
    logged_in_user = None

    while True:
        console_input = input(Fore.CYAN + '$ ').strip()

        if console_input == 'exit':
            print('')
            print(Fore.CYAN + 'Exiting Lunar...')
            time.sleep(2)
            exit()

        elif console_input == 'help':
            print('')
            print(Fore.CYAN + 'Available commands: help, exit')
            print('')

        else:
            print('')
            print(Fore.CYAN + 'Unknown command. Type "help" for help.')
            print('')

main()