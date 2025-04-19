# File name: account.py
# Date: 15/04/2025
# Written by: Mitch Coghlan


"""
    Purpose: Responsible for handling accounts inside the database
"""


from pathlib import *
from database import *


class AccountManager:
    def __init__(self, db_manager: DatabaseManager) -> None:
        # The main database manager
        self.db_manager: DatabaseManager = db_manager

    # Handle the account registration process.
    def register_account(self) -> None:
        pass

        