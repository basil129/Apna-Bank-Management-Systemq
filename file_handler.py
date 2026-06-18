"""
file_handler.py
---------------
Defines the FileHandler class for Apna Bank.
Responsible for all CSV file read and write operations.
"""

import csv
import os
from customer import Customer
from account import Account
from transaction import Transaction


class FileHandler:
    """Manages CSV-based persistence for all bank data."""

    CUSTOMERS_FILE = os.path.join("data", "customers.csv")
    ACCOUNTS_FILE = os.path.join("data", "accounts.csv")
    TRANSACTIONS_FILE = os.path.join("data", "transactions.csv")

    CUSTOMER_HEADERS = ["customer_id", "name", "email", "phone", "account_ids"]
    ACCOUNT_HEADERS = [
        "account_id", "customer_id", "account_type",
        "balance", "is_active", "created_at",
    ]
    TRANSACTION_HEADERS = [
        "transaction_id", "account_id", "transaction_type",
        "amount", "note", "timestamp",
    ]

    def __init__(self):
        """Initialise FileHandler and ensure the data directory exists."""
        os.makedirs("data", exist_ok=True)

    def save_customers(self, customers_dict):
        """
        Write all customers to the customers CSV file.

        Args:
            customers_dict (dict): Mapping of customer_id -> Customer.

        Raises:
            OSError: If the file cannot be written.
        """
        try:
            with open(self.CUSTOMERS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.CUSTOMER_HEADERS)
                for customer in customers_dict.values():
                    writer.writerow(customer.to_csv_row())
        except OSError as e:
            raise OSError(f"Failed to save customers: {e}")

    def save_accounts(self, accounts_dict):
        """
        Write all accounts to the accounts CSV file.

        Args:
            accounts_dict (dict): Mapping of account_id -> Account.

        Raises:
            OSError: If the file cannot be written.
        """
        try:
            with open(self.ACCOUNTS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.ACCOUNT_HEADERS)
                for account in accounts_dict.values():
                    writer.writerow(account.to_csv_row())
        except OSError as e:
            raise OSError(f"Failed to save accounts: {e}")

    def save_transactions(self, transactions_list):
        """
        Write all transactions to the transactions CSV file.

        Args:
            transactions_list (list): List of Transaction objects.

        Raises:
            OSError: If the file cannot be written.
        """
        try:
            with open(
                self.TRANSACTIONS_FILE, "w", newline="", encoding="utf-8"
            ) as f:
                writer = csv.writer(f)
                writer.writerow(self.TRANSACTION_HEADERS)
                for txn in transactions_list:
                    writer.writerow(txn.to_csv_row())
        except OSError as e:
            raise OSError(f"Failed to save transactions: {e}")

    def save_all(self, bank):
        """
        Save all bank data to CSV files.

        Args:
            bank (Bank): The Bank instance whose data is to be saved.
        """
        self.save_customers(bank.customers)
        self.save_accounts(bank.accounts)
        self.save_transactions(bank.transactions)

    def load_customers(self):
        """
        Read customers from the CSV file.

        Returns:
            dict: Mapping of customer_id -> Customer.

        Raises:
            OSError: If the file cannot be read.
        """
        customers = {}
        if not os.path.exists(self.CUSTOMERS_FILE):
            return customers
        try:
            with open(self.CUSTOMERS_FILE, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header row
                for row in reader:
                    if len(row) == 5:
                        customer = Customer.from_csv_row(row)
                        customers[customer.customer_id] = customer
        except OSError as e:
            raise OSError(f"Failed to load customers: {e}")
        return customers

    def load_accounts(self):
        """
        Read accounts from the CSV file.

        Returns:
            dict: Mapping of account_id -> Account.

        Raises:
            OSError: If the file cannot be read.
        """
        accounts = {}
        if not os.path.exists(self.ACCOUNTS_FILE):
            return accounts
        try:
            with open(self.ACCOUNTS_FILE, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header row
                for row in reader:
                    if len(row) == 6:
                        account = Account.from_csv_row(row)
                        accounts[account.account_id] = account
        except OSError as e:
            raise OSError(f"Failed to load accounts: {e}")
        return accounts

    def load_transactions(self):
        """
        Read transactions from the CSV file.

        Returns:
            list: List of Transaction objects.

        Raises:
            OSError: If the file cannot be read.
        """
        transactions = []
        if not os.path.exists(self.TRANSACTIONS_FILE):
            return transactions
        try:
            with open(
                self.TRANSACTIONS_FILE, "r", newline="", encoding="utf-8"
            ) as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header row
                for row in reader:
                    if len(row) == 6:
                        txn = Transaction.from_csv_row(row)
                        transactions.append(txn)
        except OSError as e:
            raise OSError(f"Failed to load transactions: {e}")
        return transactions

    def load_all(self, bank):
        """
        Load all persisted data into a Bank instance.

        Args:
            bank (Bank): The Bank instance to populate.
        """
        bank.customers = self.load_customers()
        bank.accounts = self.load_accounts()
        bank.transactions = self.load_transactions()
