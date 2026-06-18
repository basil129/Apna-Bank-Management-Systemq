"""
transaction.py
--------------
Defines the Transaction class for Apna Bank.
Records every financial event with a type, amount, and timestamp.
"""

from datetime import datetime


class Transaction:
    """Represents a single financial transaction on an account."""

    VALID_TYPES = ("deposit", "withdrawal", "transfer_in", "transfer_out")

    def __init__(self, transaction_id, account_id, transaction_type, amount, note=""):
        """
        Initialise a Transaction instance.

        Args:
            transaction_id (str): Unique transaction identifier.
            account_id (str): The account this transaction belongs to.
            transaction_type (str): One of VALID_TYPES.
            amount (float): The monetary amount involved.
            note (str): Optional description or reference.

        Raises:
            ValueError: If transaction_type is not valid.
            ValueError: If amount is not positive.
        """
        if transaction_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid transaction type '{transaction_type}'. "
                f"Choose from: {self.VALID_TYPES}."
            )
        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.note = note
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_summary(self):
        """
        Return a one-line summary of the transaction.

        Returns:
            str: Short transaction summary.
        """
        direction = "+" if self.transaction_type in (
            "deposit", "transfer_in"
        ) else "-"
        return (
            f"[{self.timestamp}] "
            f"{self.transaction_type.upper():15s} "
            f"{direction}£{self.amount:.2f}"
            + (f"  | {self.note}" if self.note else "")
        )

    def get_details(self):
        """
        Return a full formatted view of the transaction.

        Returns:
            str: Detailed transaction information.
        """
        return (
            f"Transaction ID : {self.transaction_id}\n"
            f"Account ID     : {self.account_id}\n"
            f"Type           : {self.transaction_type.replace('_', ' ').capitalize()}\n"
            f"Amount         : £{self.amount:.2f}\n"
            f"Note           : {self.note if self.note else 'N/A'}\n"
            f"Timestamp      : {self.timestamp}"
        )

    def is_credit(self):
        """
        Check whether this transaction credits the account.

        Returns:
            bool: True if deposit or transfer_in.
        """
        return self.transaction_type in ("deposit", "transfer_in")

    def is_debit(self):
        """
        Check whether this transaction debits the account.

        Returns:
            bool: True if withdrawal or transfer_out.
        """
        return self.transaction_type in ("withdrawal", "transfer_out")

    def to_csv_row(self):
        """
        Serialise the transaction to a list for CSV writing.

        Returns:
            list: Fields representing this transaction.
        """
        return [
            self.transaction_id,
            self.account_id,
            self.transaction_type,
            f"{self.amount:.2f}",
            self.note,
            self.timestamp,
        ]

    @staticmethod
    def from_csv_row(row):
        """
        Create a Transaction instance from a CSV row.

        Args:
            row (list): A list of string fields read from a CSV file.

        Returns:
            Transaction: A reconstructed Transaction instance.
        """
        txn = Transaction(
            transaction_id=row[0],
            account_id=row[1],
            transaction_type=row[2],
            amount=float(row[3]),
            note=row[4],
        )
        txn.timestamp = row[5]
        return txn
