# File name: main.py
# Written by: Mitch Coghlan on 15/04/2025


"""
    Description: The main program
"""

from user_interface import UserInterface
from pathlib import Path


# The location pointing to the database.
database_path: Path = Path("./test_data/accounts.txt")


class App:
    # Setup everything before continuing
    def __init__(self, path: Path, break_upon_error: bool = False) -> None:
        # Settings
        self.path = path
        self.break_upon_error = break_upon_error

    
    def run(self) -> None:
        """
            Run the program.    
        """

        # Create the user interface
        ui: UserInterface = UserInterface(self.path, self.break_upon_error)
        ui.run()


if __name__ == "__main__":
    app: App = App(database_path, True)
    app.run()