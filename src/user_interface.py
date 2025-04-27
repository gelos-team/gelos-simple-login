# File name: user_interface.py
# Written by: Mitch Coghlan on 27/04/2025


"""
    Description: The user interface for the login program.
"""

from pathlib import *
from database import *
from account import *
import string
import time
import sys


class MenuOption:
    def __init__(self, label: str, alias: str | list[str], command: callable, visible: bool = True) -> None:
        # Settings
        self.label: str = label
        self.alias: str | list[str] = alias
        self.command: callable = command
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
    def __check_alias__(self, alias: str | list[str]) -> None:
        match type(alias).__name__:
            case "str":
                is_singular_character: bool = self.__is_single_character__(alias)
                isnt_symbol: bool = self.__is_letter_or_number__(alias)


                # Print an error message if it isn't a singular
                # character.
                if not is_singular_character:
                    raise Exception("The alias must be one character in length.")
                
                
                # Do the same thing if the alias isn't a letter or number,
                if not isnt_symbol:
                    raise Exception("The alias must be a letter (a-z, A-Z) or number (0-9)")
        
            case "list":
                for letter in alias:
                    # Print an error message if the alias isn't valid text.
                    if type(letter) != str:
                        raise TypeError("The alias must be of type 'str'")
                    
                
                    is_singular_character: bool = self.__is_single_character__(letter)
                    isnt_symbol: bool = self.__is_letter_or_number__(letter)


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
        except Exception as err:
            raise type(err)(str(err))


# The main user interface
class UserInterface:
    def __init__(self, database_path: Path | str, break_upon_error: bool = False) -> None:
        # For logging in, account registration, checking if the user is logged in and viewing the list of accounts.
        self.account_manager: AccountManager = AccountManager(DatabaseManager(database_path, break_upon_error), break_upon_error)

        # The list of menu options
        self.menu_options: list[MenuOption] = []

        # Check if the user is logged in.
        self.is_user_logged_in = False


    # Add a menu option.
    def add_menu_option(self, label: str, alias: str | list[str], command: callable, visible: bool = True) -> None:
        self.menu_options.append(MenuOption(label, alias, command, visible))

    
    # Display the list of options
    def display_options(self) -> None:
        output: str = ""


        for option in self.menu_options:
            # Skip any invisible options
            if not option.visible:
                continue

            # List any aliases that the option uses.
            __alias__: str = ""


            if type(option.alias).__name__ == "list":
                for alias in option.alias:
                    if option.alias.index(alias) < len(option.alias) - 1:
                        __alias__ += alias + ", "
                        continue

                    __alias__ += alias
            elif type(option.alias).__name__ == "str":
                __alias__ = option.alias
            else:
                continue


            # Now output the list of options
            output += f"[{__alias__}]: {option.label}\n"


        
        print(output)

                    
    # Add a predefined list of options for the menu
    def __add_predefined_options__(self) -> None:
        self.add_menu_option("Log in", "1", self.account_manager.login)
        self.add_menu_option("Sign up", "2", self.account_manager.register_account)
        self.add_menu_option("View list of users", "3", self.account_manager.view_list)
        self.add_menu_option("Quit", "Q", exit)

    
    def run(self) -> None:
        # Create the predefined list of options
        self.__add_predefined_options__()

        while True:
            # Check if the user is logged in.
            self.is_user_logged_in = self.account_manager.is_logged_in()

            # Display the list of options
            self.display_options()

            # Prompt the user to choose an option.
            user_input: str = input("Choose an option from the list: ")


            # Do something when an option is selected.
            for option in self.menu_options:
                match type(option.alias).__name__:
                    case "str":
                        if user_input.strip() != option.alias:
                            continue

                        option.run()
                    
                    case "list":
                        for alias in option.alias:
                            if user_input.strip() != alias:
                                continue

                            option.run()
                    

