"""
customer.py
-----------
Defines the Customer class for Apna Bank.
Each customer has personal details and a list of linked account IDs.
"""


class Customer:
    """Represents a bank customer with personal details and linked accounts."""

    def __init__(self, customer_id, name, email, phone):
        """
        Initialise a Customer instance.

        Args:
            customer_id (str): Unique identifier for the customer.
            name (str): Full name of the customer.
            email (str): Email address of the customer.
            phone (str): Phone number of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.account_ids = []  # List of account IDs linked to this customer

    def add_account(self, account_id):
        """
        Link an account ID to this customer.

        Args:
            account_id (str): The account ID to link.
        """
        if account_id not in self.account_ids:
            self.account_ids.append(account_id)

    def remove_account(self, account_id):
        """
        Unlink an account ID from this customer.

        Args:
            account_id (str): The account ID to remove.

        Raises:
            ValueError: If the account ID is not linked to this customer.
        """
        if account_id not in self.account_ids:
            raise ValueError(
                f"Account '{account_id}' is not linked to "
                f"customer '{self.customer_id}'."
            )
        self.account_ids.remove(account_id)

    def update_contact(self, email=None, phone=None):
        """
        Update the customer's contact information.

        Args:
            email (str, optional): New email address.
            phone (str, optional): New phone number.
        """
        if email:
            self.email = email
        if phone:
            self.phone = phone

    def get_details(self):
        """
        Return a formatted string of the customer's details.

        Returns:
            str: Customer details as a readable string.
        """
        accounts = ", ".join(self.account_ids) if self.account_ids else "None"
        return (
            f"Customer ID : {self.customer_id}\n"
            f"Name        : {self.name}\n"
            f"Email       : {self.email}\n"
            f"Phone       : {self.phone}\n"
            f"Accounts    : {accounts}"
        )

    def to_csv_row(self):
        """
        Serialise the customer to a list for CSV writing.

        Returns:
            list: Fields representing this customer.
        """
        return [
            self.customer_id,
            self.name,
            self.email,
            self.phone,
            "|".join(self.account_ids),
        ]

    @staticmethod
    def from_csv_row(row):
        """
        Create a Customer instance from a CSV row.

        Args:
            row (list): A list of string fields read from a CSV file.

        Returns:
            Customer: A reconstructed Customer instance.
        """
        customer = Customer(
            customer_id=row[0],
            name=row[1],
            email=row[2],
            phone=row[3],
        )
        # Account IDs are stored as pipe-separated values
        if row[4]:
            customer.account_ids = row[4].split("|")
        return customer
