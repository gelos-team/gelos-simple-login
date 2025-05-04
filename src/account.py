# File name: account.py
# Written by: Mitch Coghlan on 15/04/2025


"""
    Description: Responsible for handling accounts inside the database
"""


from database import DatabaseManager
from getpass import getpass
import string
import sys
import os


class InvalidCredentialsError(Exception):
    pass


class LoginError(Exception):
    pass


class AccountCreationError(Exception):
    pass


class AccountCreationCancelled(Exception):
    pass


class LoginCancelled(Exception):
    pass


# Print an error message.
def print_error(msg: object) -> None:
    """Prints an error message to the console."""
    sys.stderr.write("ERROR: " + str(msg) + "\n")


# Clear the console window
def clear_console() -> None:
    try:
        os.system("cls" if sys.platform == "win32" else "clear")
    except:
        print("\033[2J\033[H")


class AccountManager:
    def __init__(self, db_manager: DatabaseManager, break_upon_error: bool = False) -> None:
        # The main database manager
        self.db_manager: DatabaseManager = db_manager
        self.break_upon_error: bool = break_upon_error

        self.current_account: str = ""


    # Check if the user is logged in.
    def is_logged_in(self) -> bool:
        """Checks if the user is logged in by reading through the database and seeing if the current username exists."""
        # Do nothing if the database is empty or non-existant
        if self.db_manager.is_database_empty_or_nonexistent():
            return False


        # Check if the user is logged in.
        for account in self.db_manager.read().split("\n"):
            # Get the username and check if there is a match.
            if self.current_account == account.split(",")[0].strip():
                return True
        

        return False


    # Check if the password meets the requirements
    def password_meets_requirements(self, password: str) -> None:
        """Checks if the user's password meets the requirements
defined in the Microsoft Password Complexity Standards.
        """

        # Check if the password requirements are met
        has_lowercase_letters: bool = False
        has_uppercase_letters: bool = False
        has_numbers: bool = False
        has_symbols: bool = False


        for letter in password:
            # Check if the password has lower and uppercase letters.
            if letter in string.ascii_lowercase:
                has_lowercase_letters = True

            elif letter in string.ascii_uppercase:
                has_uppercase_letters = True

            elif letter in string.digits:
                has_numbers = True

            elif letter in string.punctuation:
                has_symbols = True

        
        return (has_lowercase_letters and \
                has_uppercase_letters and \
                has_numbers and \
                has_symbols) and \
                len(password) >= 8


    # Handle the account registration process.
    def register_account(self) -> None:
        """
        Prompts the user to enter a username and password for the account they are creating. Then creates the account using the details provided and adds it to the database.
        """

        running: bool = True


        while running:
            try:
                # Container for the list of accounts
                account_list: list[dict] = []


                # Read from the database if it exists and isn't empty
                if not self.db_manager.is_database_empty_or_nonexistent():
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
                    raise InvalidCredentialsError("Please enter a username.\n")


                # Check if the username is available.
                # Restart if the username isn't.
                if not self.db_manager.is_database_empty_or_nonexistent():
                    username_available: bool = True

                    for account in account_list:
                        if username == account.get("username"):
                            username_available = False
                            break

                    if not username_available:
                        raise InvalidCredentialsError(f"The username {username} is already taken. Please choose a different one and try again.")


                # Now ask the user to enter a password for 
                # the account.
                password: str = getpass("Now enter a password: ").strip()


                # Restart if the password requirements
                # haven't been met.
                if not self.password_meets_requirements(password):
                    raise InvalidCredentialsError("Password must be 8 characters long and contain lowercase letters, uppercase letters, numbers and symbols.")

                
                # Check if the password is entered correctly.
                password_2: str = getpass("Verify password: ")


                if password != password_2:
                    raise InvalidCredentialsError("Passwords don't match.")
                    

                self.db_manager.write(self.db_manager.read() + f"\n{username},{password}")
                self.db_manager.write(self.db_manager.read())

                break

            
            except KeyboardInterrupt:
                raise AccountCreationCancelled
            

            except InvalidCredentialsError as err:
                clear_console()
                print_error(str(err))
                continue


            except Exception as err:
                if self.break_upon_error: # Print an error message if specified.
                    raise
                

                # Otherwise, stop the login process
                print_error("Something went wrong: " + str(err))
                return


    # Handle the log in process.
    def login(self) -> None:
        """Prompts the user to enter a username and password and attempts to log the user into the account if the details match."""

        running: bool = True


        while running:
            try:
                # Exit if the database doesn't exist
                if not self.db_manager.path.exists:
                    raise LoginError("The database couldn't be found inside the system.")
                

                # Read from the database
                database_contents: str = self.db_manager.read()


                # Exit if the database is empty.
                if len(database_contents) <= 0:
                    raise LoginError("The database doesn't have any entries stored.")
                

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
                    raise InvalidCredentialsError(f"An account by the username '{username}' doesn't exist.")


                # Prompt the user to enter a password for the account.
                password: str = getpass("Enter password: ")


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
                    raise InvalidCredentialsError("Incorrect password. Please try again.")


                # Log in using the account details and exit.
                self.current_account = username

                break


            except KeyboardInterrupt:
                raise LoginCancelled

                
            except InvalidCredentialsError as err:
                clear_console()
                print_error(str(err))
                continue


            except Exception as err:
                if self.break_upon_error: # Print an error message if specified.
                    raise
                
                # Otherwise, stop the login process
                print_error("Something went wrong: " + str(err))
                return


    # View list of accounts without their passwords.
    def view_list(self) -> None:
        """Reads from the database and displays a list of users.
The user needs to be logged in before viewing the list."""

        try:
            # Stop if either the database doesn't exist or is empty.
            if self.db_manager.is_database_empty_or_nonexistent():
                print("The list is currently empty.")
                return


            # Stop if the user isn't logged in.
            if not self.is_logged_in():
                raise InvalidCredentialsError("Please log in or sign up for an account before continuing.")

            
            # Display a list of users without their passwords.
            list_of_users: str = ""
            index: int = 1 # The list index


            for account in self.db_manager.read().split("\n"):
                try:
                    # Get the username from the account
                    username: str = account.split(",")[0].strip()

                    # Now add the username to the list
                    list_of_users += f"#{index}: {username}\n"
                except Exception as err: # Skip if an error had occurred
                    continue

                index += 1


            print(f"""List of user accounts

--------------------------------

{list_of_users}""")

        except InvalidCredentialsError as err:
            print_error(str(err))
            return

        except Exception as err:
            if self.break_upon_error: # Print an error message if specified.
                raise type(err)(str(err))
            
            # Otherwise, stop the login process
            sys.stderr.write("Something went wrong: " + str(err))
            return
        

        input("Press enter to continue")

                






                        

                