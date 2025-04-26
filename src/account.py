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


class InvalidCredentialsError(Exception):
    pass


# Print an error message.
def print_error(msg: object) -> None:
    sys.stderr.write("ERROR: " + str(msg) + "\n")


class AccountManager:
    def __init__(self, db_manager: DatabaseManager, break_upon_error: bool = False) -> None:
        # The main database manager
        self.db_manager: DatabaseManager = db_manager
        self.break_upon_error: bool = break_upon_error
        self.current_account: str = ""
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
                    raise InvalidCredentialsError("ERROR: Please enter a username.\n")


                # Check if the username is available.
                # Restart if the username isn't.
                if database_exists and not database_empty:
                    username_available: bool = True

                    for account in account_list:
                        if username == account.get("username"):
                            username_available = False
                            break

                    if not username_available:
                        raise InvalidCredentialsError(f"The username {username} is not available. Please choose a different one and try again.")


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
                    raise InvalidCredentialsError("Password must have atleast 8 characters, lowercase letters, uppercase letters, numbers and symbols.")

                
                # Check if the password is entered correctly.
                password_2: str = getpass("Verify password: ")


                if password != password_2:
                    raise InvalidCredentialsError("Passwords do not match. Please try again.")
                    


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

            except InvalidCredentialsError as err:
                print_error(str(err))
                continue

            except KeyboardInterrupt:
                print("\nAccount creation cancelled")
                running = False
                break

            except Exception as err:
                if self.break_upon_error: # Print an error message if specified.
                    raise type(err)(str(err))
                
                # Otherwise, stop the login process
                print_error("Something went wrong: " + str(err))
                return


    # Handle the log in process.
    def login(self) -> None:   
        running: bool = True


        while running:
            try:
                # Exit if the database doesn't exist
                if not self.db_manager.path.exists:
                    sys.stderr.write("ERROR: The database doesn't exist at the moment.\n")
                    return
                

                # Read from the database
                database_contents: str = self.db_manager.read().strip()


                # Exit if the database is empty.
                if len(database_contents) <= 0:
                    sys.stderr.write("ERROR: The database is currently empty.\n")
                    return
                


                # Prompt the user to enter a username
                username: str = input("Enter a username: ").strip()


                # Check if the username is correct
                username_matches: bool = False

                for account in database_contents.split("\n"):
                    # Get the username from the account
                    account_username: str = account.split(",")[0]


                    # Continue if the username matches
                    if username == account_username:
                        username_matches = True
                        break


                
                # Restart if there isn't a match.
                if not username_matches:
                    raise InvalidCredentialsError(f"The username {username} doesn\'t exist. Please try again.")


                # Prompt the user to enter a password for the account.
                password: str = getpass("Enter a password for " + username + ": ")


                is_password_correct: bool = False

                for account in database_contents.split("\n"):
                    # Get the username from the account
                    account_username: str = account.split(",")[0]
                    account_password: str = account.split(",")[1]


                    # Continue if the username matches
                    if username == account_username and password == account_password:
                        is_password_correct = True
                        break
                

                # Restart if the password is incorrect
                if not is_password_correct:
                    raise InvalidCredentialsError("Password is incorrect. Please try again.")


                # Log in using the account details and exit.
                self.current_account = username
                print("Account logged in successfully.")

                running = False
                break
                
            except InvalidCredentialsError as err:
                print_error(str(err))
                continue


            except KeyboardInterrupt:
                print("\nLog in cancelled")
                running = False
                break
            except Exception as err:
                if self.break_upon_error: # Print an error message if specified.
                    raise type(err)(str(err))
                
                # Otherwise, stop the login process
                print_error("Something went wrong: " + str(err))
                return
                
    # View list of accounts without their passwords.
    def view_list(self) -> None:
        try:
            # Stop if either the database doesn't exist or is empty.
            if not self.db_manager.path.exists or len(self.db_manager.read()) <= 0:
                print("There is nothing there.")
                return
            

            # Check if the user is logged in.
            is_logged_in: bool = False

            for account in self.db_manager.read().split("\n"):
                # Get the username and check if there is a match.
                if self.current_account == account.split(",")[0].strip():
                    is_logged_in = True
                    break

            if not is_logged_in:
                raise InvalidCredentialsError("You must log yourself in before viewing the list of users.")

            
            # Display a list of users without their passwords.
            list_of_users: str = ""

            index: int = 1 # The list index


            for account in self.db_manager.read().strip().split("\n"):
                try:
                    # Get the username from the account
                    username: str = account.split(",")[0].strip()

                    # Now add the username to the list
                    list_of_users += f"{index}: {username}\n"
                except Exception as err: # Skip if an error had occurred
                    continue

                index += 1


            print(list_of_users.strip())

        except InvalidCredentialsError as err:
            print_error(str(err))
            return

        except Exception as err:
            if self.break_upon_error: # Print an error message if specified.
                raise type(err)(str(err))
            
            # Otherwise, stop the login process
            sys.stderr.write("Something went wrong: " + str(err))
            return

                






                        

                