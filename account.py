"""
account.py
----------
Defines the Account class for Apna Bank.
Handles deposits, withdrawals, balance enquiries, and account status.
"""

from datetime import datetime


class Account:
    """Represents a bank account belonging to a customer."""

    VALID_TYPES = ("savings", "current")

    def __init__(self, account_id, customer_id, account_type, balance=0.0):
        """
        Initialise an Account instance.

        Args:
            account_id (str): Unique account identifier.
            customer_id (str): ID of the owning customer.
            account_type (str): Either 'savings' or 'current'.
            balance (float): Opening balance (default 0.0).

        Raises:
            ValueError: If account_type is not valid.
            ValueError: If opening balance is negative.
        """
        if account_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid account type '{account_type}'. "
                f"Choose from: {self.VALID_TYPES}."
            )
        if balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        self.account_id = account_id
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance
        self.is_active = True
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def deposit(self, amount):
        """
        Deposit money into the account.

        Args:
            amount (float): Amount to deposit. Must be positive.

        Raises:
            ValueError: If amount is not positive.
            PermissionError: If the account is inactive.
        """
        if not self.is_active:
            raise PermissionError(
                f"Account '{self.account_id}' is inactive. Cannot deposit."
            )
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraw money from the account.

        Args:
            amount (float): Amount to withdraw.

        Raises:
            ValueError: If amount is not positive or exceeds balance.
            PermissionError: If the account is inactive.
        """
        if not self.is_active:
            raise PermissionError(
                f"Account '{self.account_id}' is inactive. Cannot withdraw."
            )
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError(
                f"Insufficient funds. Available balance: £{self.balance:.2f}."
            )
        self.balance -= amount

    def get_balance(self):
        """
        Return the current balance of the account.

        Returns:
            float: Current balance.
        """
        return self.balance

    def deactivate(self):
        """
        Deactivate (close) the account.

        Raises:
            PermissionError: If the account is already inactive.
        """
        if not self.is_active:
            raise PermissionError(
                f"Account '{self.account_id}' is already inactive."
            )
        self.is_active = False

    def get_details(self):
        """
        Return a formatted string of the account's details.

        Returns:
            str: Account details as a readable string.
        """
        status = "Active" if self.is_active else "Inactive"
        return (
            f"Account ID  : {self.account_id}\n"
            f"Customer ID : {self.customer_id}\n"
            f"Type        : {self.account_type.capitalize()}\n"
            f"Balance     : £{self.balance:.2f}\n"
            f"Status      : {status}\n"
            f"Opened      : {self.created_at}"
        )

    def to_csv_row(self):
        """
        Serialise the account to a list for CSV writing.

        Returns:
            list: Fields representing this account.
        """
        return [
            self.account_id,
            self.customer_id,
            self.account_type,
            f"{self.balance:.2f}",
            str(self.is_active),
            self.created_at,
        ]

    @staticmethod
    def from_csv_row(row):
        """
        Create an Account instance from a CSV row.

        Args:
            row (list): A list of string fields read from a CSV file.

        Returns:
            Account: A reconstructed Account instance.
        """
        account = Account(
            account_id=row[0],
            customer_id=row[1],
            account_type=row[2],
            balance=float(row[3]),
        )
        account.is_active = row[4] == "True"
        account.created_at = row[5]
        return account
