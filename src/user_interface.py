# File name: user_interface.py
# Written by: Mitch Coghlan on 27/04/2025


"""
    Description: The user interface for the login program.
"""


from pathlib import Path
from database import DatabaseManager
from account import AccountManager, InvalidCredentialsError, LoginError, AccountCreationError, LoginCancelled, AccountCreationCancelled
from typing import Callable
import string
import sys
import os


class MenuOption:
    def __init__(self, label: str, id: str, alias: str, command: Callable, visible: bool = True) -> None:
        # Settings
        self.label: str = label
        self.id: str = id
        self.alias: str = alias
        self.command: Callable = command
        self.visible: bool = visible


        # Check if the alias is valid
        self.__check_alias__(self.alias)


    # Check if a character is a valid letter or a number.
    def __is_letter_or_number__(self, character: str) -> bool:
        return character in string.ascii_letters or character in string.digits


    # Check if the length of a string of text is equal to a single character.
    def __is_single_character__(self, text: str) -> bool:
        return len(text) == 1

    
    # Check if the length of the alias is equal to one character and is either a letter or a number.
    def __check_alias__(self, alias: str) -> None:
        is_singular_character: bool = self.__is_single_character__(alias)
        isnt_symbol: bool = self.__is_letter_or_number__(alias)


        # Print an error message if it isn't a singular
        # character.
        if not is_singular_character:
            raise Exception("The alias must be one character in length.")
        
        
        # Do the same thing if the alias isn't a letter or number,
        if not isnt_symbol:
            raise Exception("The alias must be a letter (a-z, A-Z) or number (0-9)")


    # Do something if told so.
    def run(self) -> None:
        try:
            self.command()


        except KeyboardInterrupt:
            clear_console()
            return


        except Exception as err:
            raise


# Clear the console window
def clear_console() -> None:
    os.system("cls" if sys.platform == "win32" else "clear")
    print("\033[2J\033[H")
    

# The main user interface
class UserInterface:
    def __init__(self, database_path: Path, break_upon_error: bool = False, quit_command: Callable = sys.exit) -> None:
        # For logging in, account registration, checking if the user is logged in and viewing the list of accounts.
        self.account_manager: AccountManager = AccountManager(DatabaseManager(database_path, break_upon_error), break_upon_error)

        # The list of menu options
        self.menu_options: list[MenuOption] = []

        # Handle quitting the application
        self.quit_command = quit_command


    # Check if a menu option already exists.
    def menu_option_exists(self, id: str) -> bool:
        """Checks if the menu option exists by reading the list and finding one based on it's ID.
Will return True if an option exists, otherwise it will return False."""


        for menu_option in self.menu_options:
            # If a menu option exists then...
            if menu_option.id == id:
                return True
        

        return False


    # Remove an option from the menu.
    def remove_menu_option(self, id: str) -> None:
        """Removes an option by looking through the list and finding one based on the ID."""


        # Skip if the option already exists
        if not self.menu_option_exists(id):
            return

        
        for option in self.menu_options:
            # Remove the menu option if there is a match
            if option.id == id:
                self.menu_options.remove(option)
                

    # Add a menu option.
    def add_menu_option(self, label: str, id: str, alias: str, command: callable, index: int = 0, visible: bool = True) -> None:
        """Adds a menu option with it's own label, ID, alias, index and whether it's visible and what it does when selected.

        
Skips if the option already exists based on it's ID"""

        
        # Skip if the option already exists
        if self.menu_option_exists(id):
            return

        
        # Otherwise, add the option to the list.
        self.menu_options.insert(index, MenuOption(label, id, alias, command, visible))


    # Clear every menu option from the list.
    def clear_menu_options(self) -> None:
        """
            Removes every menu option from the list.
        """

        for option in self.menu_options:
            self.remove_menu_option(option.id)


    # Display the list of options
    def display_options(self) -> None:
        """This method reads and displays a list of menu options including it's ID and label unless it's invisible.

Sometimes, certain options are visible if logged in."""


        output: str = ""


        for option in self.menu_options:
            # Skip any invisible options
            if not option.visible:
                continue

            
            output += f"[{option.alias.upper()}]: {option.label}\n"


        # Now output the list of options
        print(output)

                    
    # Add a predefined list of options for the menu
    def __add_predefined_options__(self) -> None:
        """
            Adds a list of predefined options to the main menu.

            The options include the option to log in, create accounts and view a list of users (when logged in).
        """

        self.add_menu_option("Login", "login", "1", self.account_manager.login, 1)
        self.add_menu_option("Register", "register", "2", self.account_manager.register_account, 2)
        self.add_menu_option("View list of accounts", "list", "3", self.account_manager.view_list, 3)
        self.add_menu_option("Quit", "quit", "q", self.quit_command, 4)
            

    # Output the heading of the program.
    def __display_header__(self) -> None:
        print(f"""Gelos Account Login
{f"Currently logged in as: {self.account_manager.current_account}" if self.account_manager.is_logged_in() else ""}
""")


    # Check if the option has symbols
    def __has_symbols__(self, text: str) -> bool:
        for letter in text:
            # Stop if there is a match.
            if letter in string.punctuation:
                return True
            
        
        return False


    def run(self) -> None:
        message: str = ""


        while True:
            # Clear the console window before continuing
            clear_console()

            # Display the heading of the program.
            self.__display_header__()

            # Create the predefined list of options
            self.__add_predefined_options__()

            # Display the list of options
            self.display_options()

            # Display a message if there is any.
            print(f"{message}\n")



            # Prompt the user to choose an option.
            user_input: str = input("Choose an option from the list: ")


            try:
                # Stop if there was no user input
                if len(user_input.strip()) <= 0:
                    message = "The option field cannot be empty."
                    continue


                # Check if there isn't a symbol in the input.
                if self.__has_symbols__(user_input):
                    message = "The option field must not contain symbols."
                    continue


                # Stop if the input is longer than 1 character
                if len(user_input) > 1:
                    message = "The option must be 1 character in length."
                    continue


                # Print a message if an incorrect option was selected.
                is_option_valid: bool = False


                # Do something when an option is selected.
                for option in self.menu_options:
                    if user_input.upper().strip() != option.alias.upper():
                        is_option_valid = False
                        continue


                    # Clear the console before continuing
                    clear_console()
                    

                    # Do something if an option has been selected.
                    is_option_valid = True

                    # Clear the message before doing anything
                    message = ""


                    option.run()
                    break


                if not is_option_valid:
                    message = "Please choose a valid option from the list."

            
            except InvalidCredentialsError as err:
                message = str(err)
                continue


            except LoginError as err:
                message = str(err)
                continue


            except AccountCreationError as err:
                message = str(err)
                continue


            except LoginError as err:
                message = str(err)
                continue


            except AccountCreationCancelled:
                message = "Account creation cancelled."
                continue


            except LoginCancelled:
                message = "Login cancelled."
                continue


            except Exception as err:
                # Ignore if exitting the program.
                if type(err) is SystemExit:
                    pass

                message = "Something went wrong."
                continue