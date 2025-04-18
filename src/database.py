# File name: database.py
# Date: 15/04/2025
# Written by: Mitch Coghlan


"""
    Purpose: Responsible for reading and writing to and from the database
"""

from pathlib import *
import os
import sys


# Print an error message.
def print_error(msg: object) -> None:
    sys.stderr.write("ERROR: " + str(msg) + "\n")

class DatabaseReadError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)

class DatabaseWriteError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


class DatabaseManager:
    def __init__(self, database_path: Path | str, break_upon_error: bool = False) -> None:
        # The location leading to the database
        self.path: Path = Path(database_path) if type(database_path) == str else database_path

        # Stop if an error occurred unless told otherwise
        self.break_upon_error = break_upon_error

    
    # Read the contents from the database.
    def __read__(self, path: Path, break_upon_error: bool = False) -> str:
        # Check if the database file exists inside the storage device.
        if not path.exists:
            raise FileNotFoundError("The database at " + str(path.resolve()) + " could not be found.") if break_upon_error else print_error("The database could not be found.")

            return ""


        try:
            # Try and read from the database
            with path.open() as database:
                return database.read()
        except Exception as err:
            # Print an error message unless said otherwise.
            if break_upon_error:
                raise DatabaseReadError(str(type(err).__name__) + " - " + str(err))


            return ""


    def read(self) -> str:
        return self.__read__(self.path, self.break_upon_error)