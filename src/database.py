# File name: database.py
# Date: 15/04/2025
# Written by: Mitch Coghlan


"""
    Purpose: Responsible for reading and writing to and from the database
"""

from pathlib import *
import os


class DatabaseReadError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


class Account:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class DatabaseManager:
    def __init__(self, database_path: Path | str, break_upon_error: bool = False) -> None:
        # The location leading to the database
        self.path: Path = Path(database_path) if type(database_path) == str else database_path

        # Stop if an error occurred unless told otherwise
        self.break_upon_error = break_upon_error

    
    # Read from the database
    def __read__(self, path: Path, break_upon_error: bool = False) -> list[Account]:
        try:
            # Stop if the database doesn't exist.
            if not path.exists(follow_symlinks=False):
                # Print an error message saying that the database doesn't exist.
                raise FileNotFoundError(f"The database could not be found at {path.resolve(True)}. Please check your spelling and try again.")
            
                return []
            

            # Try and read from the database.
            database_text: str = ""


            with path.open() as database_file:
                # Get the contents of the database, including the credentials of the accounts.
                database_text = database_file.read().strip()


            # Do nothing if the database is empty
            if len(database_text) <= 0:
                return []
            

            # Get the usernames and passwords from every account
            account_list: list[Account] = []


            for account in database_text.split("\n"):
                account_list.append(Account(account.strip().split(",")[0], account.strip().split(",")[1]))

            
            return account_list
        except Exception as err:
            if break_upon_error:
                raise DatabaseReadError(f"{type(err).__name__} - {err}")
            
            return []
    

    def read(self) -> list[Account]:
        return self.__read__(self.path, self.break_upon_error)