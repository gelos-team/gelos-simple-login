# File name: account.py
# Date: 15/04/2025
# Written by: Mitch Coghlan


"""
    Purpose: Responsible for handling accounts inside the database
"""


from pathlib import *
from database import *
from getpass import getpass
import string

class AccountManager:
    def __init__(self, db_manager: DatabaseManager) -> None:
        # The main database manager
        self.db_manager: DatabaseManager = db_manager

    # Handle the account registration process.
    def register_account(self) -> None:
        running: bool = True


        while running:
            try:
                # Check if the database exists.
                database_exists: bool = self.db_manager.path.exists()

                # Also check if the database is empty.
                database_empty: bool = len(self.db_manager.read()) <= 0

                # Container for the list of accounts
                account_list: list[dict] = []


                # Read from the database if it exists and isn't empty
                if database_exists and not database_empty:
                    for account in self.db_manager.read().split("\n"):
                        # Get the usernames and password from every account
                        try:
                            account_list.append({
                                "username": account.split(",")[0].strip(),
                                "password": account.split(",")[1].strip()
                            })
                        except:
                            continue

                
                # Prompt the user to enter a username
                # for the account.
                username: str = input("Enter a username for the account: ").strip()


                # Check if the username isn't empty.
                if len(username) <= 0:
                    sys.stderr.write("ERROR: Please enter a username.\n")
                    continue


                # Check if the username is available.
                # Restart if the username isn't.
                if database_exists and not database_empty:
                    username_available: bool = True

                    for account in account_list:
                        if username == account.get("username"):
                            username_available = False
                            break

                    if not username_available:
                        sys.stderr.write("ERROR: The username " + username + " is not available. Please choose a different one and try again.\n")
                        continue


                # Now ask the user to enter a password for 
                # the account.
                password: str = getpass("Enter a password for " + username + ": ").strip()

                
                # Check if the password requirements are met
                has_lowercase_letters: bool = False
                has_uppercase_letters: bool = False
                has_numbers: bool = False
                has_symbols: bool = False

                for letter in string.ascii_lowercase:
                    if letter in password:
                        has_lowercase_letters = True
                        break

                
                for letter in string.ascii_uppercase:
                    if letter in password:
                        has_uppercase_letters = True
                        break
                

                for number in string.digits:
                    if number in password:
                        has_numbers = True
                        break
                

                for symbol in string.punctuation:
                    if symbol in password:
                        has_symbols = True
                        break

                
                # Restart if the password requirements
                # haven't been met.
                if not (has_lowercase_letters and has_uppercase_letters and \
                        has_numbers and has_symbols) or len(password) < 8:
                    sys.stderr.write("ERROR: Password must have atleast 8 characters, lowercase letters, uppercase letters, numbers and symbols.\n")
                    continue

                
                # Check if the password is entered correctly.
                password_2: str = getpass("Verify password: ")


                if password != password_2:
                    sys.stderr.write("ERROR: Passwords do not match. Please try again.\n")
                    continue


                # Ask if the user wishes to create their account
                while True:
                    user_input: str = input("You want to create an account under the name " + username + \
                                                 ".\nDo you wish to continue [y/N]: ")
                    
                    if len(user_input) <= 0 or user_input.strip().lower() == "n":
                        print("Account creation cancelled")
                        running = False
                        return
                    elif user_input.strip().lower() == "y":
                        self.db_manager.write(self.db_manager.read() + f"\n{username},{password}")
                        
                        print("The account has been created successfully. You can login now.")
                        running = False
                        return
                    else:
                        sys.stderr.write("ERROR: Please choose a valid option.")

            except KeyboardInterrupt:
                print("\nAccount creation cancelled")
                running = False
                break          








                    

            