# File name: user_interface.py
# Written by: Mitch Coghlan on 27/04/2025


"""
    Description: The user interface for the login program.
"""

from pathlib import *
from database import *
from account import *
import string
import sys


class MenuOption:
    def __init__(self, label: str, alias: str | list[str], command: callable, visible: bool = True) -> None:
        # Settings
        self.label: str = label
        self.alias: str | list = alias
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
        except Exception as err:
            raise type(err)(str(err))