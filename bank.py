"""
bank.py
-------
Defines the Bank class for Apna Bank.
Central controller that manages all customers, accounts, and transactions.
"""

import uuid
from customer import Customer
from account import Account
from transaction import Transaction


class Bank:
    """
    Central controller for Apna Bank.

    Manages all customers, accounts, and transactions in memory.
    """

    def __init__(self, bank_name):
        """
        Initialise the Bank.

        Args:
            bank_name (str): Name of the bank.
        """
        self.bank_name = bank_name
        self.customers = {}     # customer_id -> Customer
        self.accounts = {}      # account_id  -> Account
        self.transactions = []  # list of Transaction objects

    # ------------------------------------------------------------------
    # Customer operations
    # ------------------------------------------------------------------

    def register_customer(self, name, email, phone):
        """
        Register a new customer.

        Args:
            name (str): Full name.
            email (str): Email address.
            phone (str): Phone number.

        Raises:
            ValueError: If any field is empty.

        Returns:
            str: The newly generated customer ID.
        """
        if not name.strip() or not email.strip() or not phone.strip():
            raise ValueError("Name, email, and phone are all required.")

        customer_id = "C" + str(uuid.uuid4())[:8].upper()
        customer = Customer(
            customer_id,
            name.strip(),
            email.strip(),
            phone.strip(),
        )
        self.customers[customer_id] = customer
        return customer_id

    def get_customer(self, customer_id):
        """
        Retrieve a customer by ID.

        Args:
            customer_id (str): The customer's ID.

        Raises:
            KeyError: If no customer with that ID exists.

        Returns:
            Customer: The matching Customer object.
        """
        if customer_id not in self.customers:
            raise KeyError(f"Customer '{customer_id}' not found.")
        return self.customers[customer_id]

    def list_customers(self):
        """
        Return all registered customers.

        Returns:
            list[Customer]: All customers in the system.
        """
        return list(self.customers.values())

    def update_customer_contact(self, customer_id, email=None, phone=None):
        """
        Update a customer's contact details.

        Args:
            customer_id (str): The customer's ID.
            email (str, optional): New email address.
            phone (str, optional): New phone number.
        """
        customer = self.get_customer(customer_id)
        customer.update_contact(email=email, phone=phone)

    # ------------------------------------------------------------------
    # Account operations
    # ------------------------------------------------------------------

    def open_account(self, customer_id, account_type, initial_deposit=0.0):
        """
        Open a new account for an existing customer.

        Args:
            customer_id (str): The owning customer's ID.
            account_type (str): 'savings' or 'current'.
            initial_deposit (float): Opening balance (default 0.0).

        Raises:
            KeyError: If the customer does not exist.
            ValueError: If account_type or initial_deposit is invalid.

        Returns:
            str: The newly generated account ID.
        """
        customer = self.get_customer(customer_id)

        account_id = "A" + str(uuid.uuid4())[:8].upper()
        account = Account(account_id, customer_id, account_type, initial_deposit)
        self.accounts[account_id] = account
        customer.add_account(account_id)

        # Record the opening deposit as a transaction if amount > 0
        if initial_deposit > 0:
            self._record_transaction(
                account_id, "deposit", initial_deposit, note="Opening deposit"
            )
        return account_id

    def get_account(self, account_id):
        """
        Retrieve an account by ID.

        Args:
            account_id (str): The account's ID.

        Raises:
            KeyError: If no account with that ID exists.

        Returns:
            Account: The matching Account object.
        """
        if account_id not in self.accounts:
            raise KeyError(f"Account '{account_id}' not found.")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        """
        Deposit funds into an account.

        Args:
            account_id (str): Target account ID.
            amount (float): Amount to deposit.
        """
        account = self.get_account(account_id)
        account.deposit(amount)
        self._record_transaction(account_id, "deposit", amount)

    def withdraw(self, account_id, amount):
        """
        Withdraw funds from an account.

        Args:
            account_id (str): Source account ID.
            amount (float): Amount to withdraw.
        """
        account = self.get_account(account_id)
        account.withdraw(amount)
        self._record_transaction(account_id, "withdrawal", amount)

    def transfer(self, from_account_id, to_account_id, amount):
        """
        Transfer funds between two accounts.

        Args:
            from_account_id (str): Source account ID.
            to_account_id (str): Destination account ID.
            amount (float): Amount to transfer.

        Raises:
            ValueError: If both account IDs are the same.
        """
        if from_account_id == to_account_id:
            raise ValueError("Source and destination accounts cannot be the same.")

        source = self.get_account(from_account_id)
        destination = self.get_account(to_account_id)

        source.withdraw(amount)
        destination.deposit(amount)

        self._record_transaction(
            from_account_id, "transfer_out", amount,
            note=f"Transfer to {to_account_id}"
        )
        self._record_transaction(
            to_account_id, "transfer_in", amount,
            note=f"Transfer from {from_account_id}"
        )

    def close_account(self, account_id):
        """
        Deactivate an account.

        Args:
            account_id (str): The account to close.
        """
        account = self.get_account(account_id)
        account.deactivate()

    def list_accounts_for_customer(self, customer_id):
        """
        Return all accounts belonging to a specific customer.

        Args:
            customer_id (str): The customer's ID.

        Returns:
            list[Account]: The customer's accounts.
        """
        customer = self.get_customer(customer_id)
        return [
            self.accounts[aid]
            for aid in customer.account_ids
            if aid in self.accounts
        ]

    # ------------------------------------------------------------------
    # Transaction operations
    # ------------------------------------------------------------------

    def _record_transaction(self, account_id, txn_type, amount, note=""):
        """
        Internal helper to create and store a Transaction.

        Args:
            account_id (str): Associated account ID.
            txn_type (str): Transaction type string.
            amount (float): Amount involved.
            note (str): Optional description.
        """
        txn_id = "T" + str(uuid.uuid4())[:8].upper()
        txn = Transaction(txn_id, account_id, txn_type, amount, note)
        self.transactions.append(txn)

    def get_account_statement(self, account_id):
        """
        Return all transactions for a specific account.

        Args:
            account_id (str): The account's ID.

        Returns:
            list[Transaction]: Transactions for that account.
        """
        self.get_account(account_id)  # raises KeyError if not found
        return [t for t in self.transactions if t.account_id == account_id]

    def get_all_transactions(self):
        """
        Return every transaction recorded in the system.

        Returns:
            list[Transaction]: All transactions.
        """
        return self.transactions
