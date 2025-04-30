# File name: database.py
# Written by: Mitch Coghlan on 15/04/2025


"""
    Description: Responsible for reading and writing to and from the database
"""


from pathlib import Path
import os
import sys


# Print an error message.
def print_error(msg: object) -> None:
    sys.stderr.write("ERROR: " + str(msg) + "\n")


# Error message that occurs when something goes wrong while reading from the database.
class DatabaseReadError(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


# Same thing but occurs when writing to the database.
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
            # Print an error message if database doesn't exist.
            raise FileNotFoundError("The database at " + str(path.resolve()) + " could not be found.") if break_upon_error else print_error("The database could not be found.")

            return ""


        try:
            # Try and read from the database
            with path.open() as database:
                return database.read().strip()
        except Exception as err: # Output nothing if something goes wrong while reading from the database.
            # Print an error message unless said otherwise.
            if break_upon_error:
                raise DatabaseReadError(str(type(err).__name__) + " - " + str(err))


            return ""


    # Write contents to the database
    def __write__(self, path: Path, contents: str, break_upon_error: bool = False) -> None:
        try:
            # Create the file if it doesn't exist.
            if not path.exists():
                # But first, create the folders containing the file.
                for folder in path.resolve().parents:
                    # Skip if the folder already exists.
                    if folder.exists():
                        continue

                    # Otherwise, create the folder
                    os.mkdir(folder)


                # Now create and write the contents to the new
                # database file.
                with path.open("w") as database:
                    database.write(contents)

                return


            # Stop if there are no differences
            old_db_contents: str = self.__read__(path, break_upon_error)

            if contents == old_db_contents:
                return


            # Otherwise, write the new contents to the database.
            with path.open("w") as database:
                database.write(contents)

        except Exception as err: # Do nothing if something went wrong writing to the database.
            if break_upon_error:
                raise DatabaseWriteError(str(type(err).__name__) + " - " + str(err))

            return


    def read(self) -> str: # Provide a more friendlier approach to reading from the database.
        return self.__read__(self.path, self.break_upon_error)


    def write(self, contents: str) -> None: # Do the same thing but for writing to the database.
        self.__write__(self.path, contents, self.break_upon_error)


    # Check if the database is empty or non-existant
    def is_database_empty_or_nonexistent(self) -> bool:
        return not self.path.exists() or len(self.read()) <= 0