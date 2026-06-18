"""
main.py
-------
Entry point for the Apna Bank application.
Provides a menu-driven interface for all banking operations.
Data is loaded on startup and saved on exit.
"""

from bank import Bank
from file_handler import FileHandler


# ---------------------------------------------------------------------------
# Input helper functions
# ---------------------------------------------------------------------------

def get_positive_float(prompt):
    """
    Prompt the user until a valid positive float is entered.

    Args:
        prompt (str): The message to display.

    Returns:
        float: A validated positive float value.
    """
    while True:
        try:
            value = float(input(prompt).strip())
            if value <= 0:
                print("  Amount must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number.")


def get_non_empty(prompt):
    """
    Prompt the user until a non-empty string is entered.

    Args:
        prompt (str): The message to display.

    Returns:
        str: A non-empty string.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty. Try again.")


def print_separator():
    """Print a dividing line for readability."""
    print("-" * 50)


# ---------------------------------------------------------------------------
# Customer menu functions
# ---------------------------------------------------------------------------

def register_customer(bank):
    """Handle registering a new customer."""
    print("\nRegister New Customer")
    print_separator()
    name = get_non_empty("Name  : ")
    email = get_non_empty("Email : ")
    phone = get_non_empty("Phone : ")
    try:
        cid = bank.register_customer(name, email, phone)
        print(f"Customer registered. Customer ID: {cid}")
    except ValueError as e:
        print(f"Error: {e}")


def view_customer(bank):
    """Display details for a specific customer."""
    print("\nView Customer")
    print_separator()
    cid = get_non_empty("Customer ID: ")
    try:
        customer = bank.get_customer(cid)
        print()
        print(customer.get_details())
    except KeyError as e:
        print(f"Error: {e}")


def list_all_customers(bank):
    """List all registered customers."""
    print("\nAll Customers")
    print_separator()
    customers = bank.list_customers()
    if not customers:
        print("No customers registered yet.")
        return
    for c in customers:
        print(f"{c.customer_id}  |  {c.name}  |  {c.email}  |  {c.phone}")


def update_customer(bank):
    """Update a customer's email or phone number."""
    print("\nUpdate Customer Contact")
    print_separator()
    cid = get_non_empty("Customer ID: ")
    try:
        bank.get_customer(cid)
    except KeyError as e:
        print(f"Error: {e}")
        return

    print("Press Enter to keep the existing value.")
    new_email = input("New email : ").strip() or None
    new_phone = input("New phone : ").strip() or None

    if not new_email and not new_phone:
        print("No changes made.")
        return

    bank.update_customer_contact(cid, email=new_email, phone=new_phone)
    print("Contact details updated.")


# ---------------------------------------------------------------------------
# Account menu functions
# ---------------------------------------------------------------------------

def open_account(bank):
    """Open a new account for a customer."""
    print("\nOpen New Account")
    print_separator()
    cid = get_non_empty("Customer ID: ")
    try:
        bank.get_customer(cid)
    except KeyError as e:
        print(f"Error: {e}")
        return

    print("Account type: 1) Savings   2) Current")
    choice = input("Select     : ").strip()
    type_map = {"1": "savings", "2": "current"}
    if choice not in type_map:
        print("Invalid selection.")
        return

    account_type = type_map[choice]
    raw = input("Initial deposit (0 if none): ").strip()

    try:
        initial_deposit = float(raw) if raw else 0.0
        if initial_deposit < 0:
            print("Initial deposit cannot be negative.")
            return
        aid = bank.open_account(cid, account_type, initial_deposit)
        print(f"Account opened. Account ID: {aid}")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


def view_account(bank):
    """Display details for a specific account."""
    print("\nView Account")
    print_separator()
    aid = get_non_empty("Account ID: ")
    try:
        account = bank.get_account(aid)
        print()
        print(account.get_details())
    except KeyError as e:
        print(f"Error: {e}")


def list_customer_accounts(bank):
    """List all accounts for a given customer."""
    print("\nAccounts for Customer")
    print_separator()
    cid = get_non_empty("Customer ID: ")
    try:
        accounts = bank.list_accounts_for_customer(cid)
        if not accounts:
            print("No accounts found for this customer.")
            return
        for acc in accounts:
            status = "Active" if acc.is_active else "Inactive"
            print(
                f"{acc.account_id}  |  "
                f"{acc.account_type.capitalize():8}  |  "
                f"£{acc.balance:.2f}  |  {status}"
            )
    except KeyError as e:
        print(f"Error: {e}")


def close_account(bank):
    """Deactivate an account."""
    print("\nClose Account")
    print_separator()
    aid = get_non_empty("Account ID: ")
    confirm = input(f"Confirm closing '{aid}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    try:
        bank.close_account(aid)
        print("Account closed.")
    except (KeyError, PermissionError) as e:
        print(f"Error: {e}")


# ---------------------------------------------------------------------------
# Transaction menu functions
# ---------------------------------------------------------------------------

def deposit(bank):
    """Deposit money into an account."""
    print("\nDeposit")
    print_separator()
    aid = get_non_empty("Account ID : ")
    amount = get_positive_float("Amount (£) : ")
    try:
        bank.deposit(aid, amount)
        balance = bank.get_account(aid).get_balance()
        print(f"Deposited £{amount:.2f}. New balance: £{balance:.2f}")
    except (KeyError, ValueError, PermissionError) as e:
        print(f"Error: {e}")


def withdraw(bank):
    """Withdraw money from an account."""
    print("\nWithdraw")
    print_separator()
    aid = get_non_empty("Account ID : ")
    amount = get_positive_float("Amount (£) : ")
    try:
        bank.withdraw(aid, amount)
        balance = bank.get_account(aid).get_balance()
        print(f"Withdrew £{amount:.2f}. New balance: £{balance:.2f}")
    except (KeyError, ValueError, PermissionError) as e:
        print(f"Error: {e}")


def transfer(bank):
    """Transfer funds between two accounts."""
    print("\nTransfer")
    print_separator()
    from_id = get_non_empty("From Account ID : ")
    to_id = get_non_empty("To Account ID   : ")
    amount = get_positive_float("Amount (£)      : ")
    try:
        bank.transfer(from_id, to_id, amount)
        print(f"Transferred £{amount:.2f} from {from_id} to {to_id}.")
    except (KeyError, ValueError, PermissionError) as e:
        print(f"Error: {e}")


def view_statement(bank):
    """Display the transaction history for an account."""
    print("\nAccount Statement")
    print_separator()
    aid = get_non_empty("Account ID: ")
    try:
        transactions = bank.get_account_statement(aid)
        if not transactions:
            print("No transactions found for this account.")
            return
        print()
        for txn in transactions:
            print(txn.get_summary())
    except KeyError as e:
        print(f"Error: {e}")


# ---------------------------------------------------------------------------
# Main menu loop
# ---------------------------------------------------------------------------

MENU = """
Apna Bank - Main Menu
---------------------------------------------
Customer Management
  1. Register new customer
  2. View customer details
  3. List all customers
  4. Update customer contact

Account Management
  5. Open new account
  6. View account details
  7. List accounts for a customer
  8. Close account

Transactions
  9. Deposit
  10. Withdraw
  11. Transfer
  12. View account statement

  0. Save and Exit
---------------------------------------------"""

ACTIONS = {
    "1": register_customer,
    "2": view_customer,
    "3": list_all_customers,
    "4": update_customer,
    "5": open_account,
    "6": view_account,
    "7": list_customer_accounts,
    "8": close_account,
    "9": deposit,
    "10": withdraw,
    "11": transfer,
    "12": view_statement,
}


def main():
    """Run the Apna Bank application."""
    bank = Bank("Apna Bank")
    handler = FileHandler()

    # Load existing data from CSV files
    try:
        handler.load_all(bank)
        print("Data loaded successfully.")
    except OSError as e:
        print(f"Could not load existing data: {e}. Starting fresh.")

    print(f"\nWelcome to {bank.bank_name}!")

    while True:
        print(MENU)
        choice = input("Enter choice: ").strip()

        if choice == "0":
            try:
                handler.save_all(bank)
                print("Data saved. Goodbye!")
            except OSError as e:
                print(f"Error saving data: {e}")
            break
        elif choice in ACTIONS:
            ACTIONS[choice](bank)
        else:
            print("Invalid option. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
