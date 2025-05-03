# File name: main.py
# Written by: Mitch Coghlan on 15/04/2025


"""
    Description: The main program
"""

from user_interface import UserInterface, clear_console
from pathlib import Path
import sys


# The location pointing to the database.
database_path: Path = Path("./test_data/accounts.txt")


class App:
    # Setup everything before continuing
    def __init__(self, path: Path, break_upon_error: bool = False) -> None:
        # Settings
        self.path = path
        self.break_upon_error = break_upon_error


        # The main user interface.
        self.ui: UserInterface = UserInterface(self.path, self.break_upon_error, self.quit)

    # Close and exit the program.
    def quit(self) -> None:
        sys.exit()
    
    def run(self) -> None:
        """
            Run the program.    
        """

        try:
            # Create the user interface
            self.ui.run()

        # Quit the application when Ctrl+C is pressed instead of spitting out a whole heap of jargon.
        except KeyboardInterrupt:
            clear_console()
            self.quit()

        except Exception as err:
            if self.break_upon_error:
                raise
            else:
                sys.stderr.write("Something went wrong and the program has to quit.")
                sys.exit(-1)



if __name__ == "__main__":
    app: App = App(database_path, True)
    app.run()