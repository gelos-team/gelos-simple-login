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


class DatabaseManager:
    def __init__(self, database_path: Path | str, break_upon_error: bool = False) -> None:
        # The location leading to the database
        self.path: Path = Path(database_path) if type(database_path) == str else database_path


        # Stop if an error occurred unless told otherwise
        self.break_upon_error = break_upon_error

    
    # Read from the database
    def __read__(self, path: Path, break_upon_error: bool = False) -> list[dict]:
        try:
            # Stop if the database doesn't exist.
            if not os.path.exists(path):
                # Print an error message if told too
                if break_upon_error:
                    raise FileNotFoundError("The database at " + str(path.resolve()) + " doesn't exist inside the computer.")
        except Exception as err:
            # Print an error message unless said otherwise.
            if break_upon_error:
                raise DatabaseReadError(str(type(err).__name__) + ": " + str(err))
            
            # Output nothing and exit
            return []
        
    def read(self) -> list[dict]:
        return self.__read__(self.path, self.break_upon_error)