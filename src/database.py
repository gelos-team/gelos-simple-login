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


class DatabaseManager:
    def __init__(self, database_path: Path, break_upon_error: bool = False) -> None:
        # The location leading to the database
        self.path: Path = database_path

        # Stop if an error occurred unless told otherwise
        self.break_upon_error = break_upon_error


    # Check if the database is empty or non-existant
    def is_database_empty_or_nonexistent(self) -> bool:
        return not self.path.exists() or len(self.read()) <= 0


    # Read the contents from the database.
    def __read__(self, path: Path, break_upon_error: bool = False) -> str:
        # Check if the database file exists inside the storage device.
        if not path.exists():
            return "" # Output nothing if the file could not be found


        try:
            # Try and read from the database
            with path.open() as database:
                return database.read().strip()
        
        except FileNotFoundError: # Do nothing if the database could not be found.
            return ""
        
        except Exception as err: # Output nothing if something goes wrong while reading from the database.
            # Print an error message unless said otherwise.
            if break_upon_error:
                raise


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
                raise

            return


    def read(self) -> str: # Provide a more friendlier approach to reading from the database.
        return self.__read__(self.path, self.break_upon_error)


    def write(self, contents: str) -> None: # Do the same thing but for writing to the database.
        self.__write__(self.path, contents, self.break_upon_error)