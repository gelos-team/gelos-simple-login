# File name: user_interface.py
# Written by: Mitch Coghlan on 27/04/2025


"""
    Description: The user interface for the login program.
"""


from pathlib import Path
from database import DatabaseManager
from account import AccountManager
import string
import sys
import os


class MenuOption:
    def __init__(self, label: str, id: str, alias: str | list[str], command: callable, visible: bool = True) -> None:
        # Settings
        self.label: str = label
        self.id: str = id
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
            raise


# Clear the console window
def clear_console() -> None:
    try:
        os.system("cls" if sys.platform == "win32" else "clear")
    except:
        print("\033[2J\033[H")
    

# The main user interface
class UserInterface:
    def __init__(self, database_path: Path, break_upon_error: bool = False) -> None:
        # For logging in, account registration, checking if the user is logged in and viewing the list of accounts.
        self.account_manager: AccountManager = AccountManager(DatabaseManager(database_path, break_upon_error), break_upon_error)

        # The list of menu options
        self.menu_options: list[MenuOption] = []

        # Check if the user is logged in.
        self.is_user_logged_in = False


    # Check if a menu option already exists.
    def menu_option_exists(self, id: str) -> bool:
        """
            Checks if a menu option exists by looking for it's I.D.
        """

        for menu_option in self.menu_options:
            # If a menu option exists then...
            if menu_option.id == id:
                return True
        

        return False


    # Remove an option from the menu.
    def remove_menu_option(self, id: str) -> None:
        """
            Removes a menu option based on the I.D.
        """

        # Skip if the option already exists
        if not self.menu_option_exists(id):
            return

        
        for option in self.menu_options:
            # Remove the menu option if there is a match
            if option.id == id:
                self.menu_options.remove(option)
                

    # Add a menu option.
    def add_menu_option(self, label: str, id: str, alias: str | list[str], command: callable, index: int = 0, visible: bool = True) -> None:
        """
            Adds a menu option to a list.
        """
        
        # Skip if the option already exists
        if self.menu_option_exists(id):
            return

        
        # Otherwise, add the option to the list.
        self.menu_options.insert(index, MenuOption(label, id, alias, command, visible))


    # Clear every menu option from the list.
    def clear_menu_options(self) -> None:
        """
            Removes every menu option.
        """

        for option in self.menu_options:
            self.remove_menu_option(option.id)


    # Display the list of options
    def display_options(self) -> None:
        """
            Displays a list of options to choose from.
        """


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
                        __alias__ += alias.upper() + ", "
                        continue

                    __alias__ += alias
            elif type(option.alias).__name__ == "str":
                __alias__ = option.alias.upper()
            else:
                continue


            
            output += f"[{__alias__}]: {option.label}\n"


        # Now output the list of options
        print(output)

                    
    # Add a predefined list of options for the menu
    def __add_predefined_options__(self) -> None:
        """
            Adds a list of predefined options to the main menu.

            The options include the option to log in, create accounts and view a list of users (when logged in).
        """

        # Clear everything before continuing
        self.clear_menu_options()


        # Add the options to log in or sign up
        self.add_menu_option("Log in", "login", "1", self.account_manager.login, 0) \
            if not self.account_manager.db_manager.is_database_empty_or_nonexistent() \
                else self.remove_menu_option("login")
        

        self.add_menu_option("Sign up", "register", "2", self.account_manager.register_account, 1)
        
        # Add the option to view a list of accounts when logged in.
        self.add_menu_option("View list of users", "list_user_accounts", "3", self.account_manager.view_list, 2) \
        if self.account_manager.is_logged_in() else \
        self.remove_menu_option("list_user_accounts")


        # Add the option to exit out of the program.
        self.add_menu_option("Quit", "exit", "q", exit, 3)


    def run(self) -> None:
        while True:
            # Clear the console window before continuing
            clear_console()

            # Create the predefined list of options
            self.__add_predefined_options__()

            # Display the list of options
            self.display_options()

            # Display the current username if logged in.
            if self.account_manager.is_logged_in():
                print(f"Current user: {self.account_manager.current_account}")
            else:
                print("Currently signed out.")

            # Prompt the user to choose an option.
            user_input: str = input("Choose an option from the list: ")


            # Do something when an option is selected.
            for option in self.menu_options:
                finished: bool = False

                match type(option.alias).__name__:
                    case "str":
                        if user_input.upper().strip() != option.alias.upper():
                            continue


                        # Clear the console before continuing
                        clear_console()

                        option.run()
                        finished = True

                    
                    case "list":
                        for alias in option.alias:
                            if user_input.upper().strip() != alias.upper():
                                continue

                            # Clear the console before continuing
                            clear_console()

                            option.run()
                            finished = True
                            break


                # Stop once everything is finished
                break

            # Clear everything from the console window when finished.
            clear_console()
                    

