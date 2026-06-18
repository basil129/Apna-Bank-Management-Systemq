# Apna Bank - Banking System

This is a simple banking system I built using Python for my B100 module at Gisma University of Applied Sciences.

## What this project does

It lets you manage bank customers and their accounts. You can register customers, open savings or current accounts, deposit and withdraw money, transfer funds between accounts, and view transaction history. All data is saved to CSV files so nothing is lost when you close the program.

## Files in this project

- main.py - this is where you run the program from. It shows the menu and handles user input
- bank.py - contains the Bank class which controls all the main operations
- customer.py - contains the Customer class
- account.py - contains the Account class
- transaction.py - contains the Transaction class
- file_handler.py - handles reading and writing data to CSV files
- data/customers.csv - stores customer records
- data/accounts.csv - stores account records
- data/transactions.csv - stores transaction records

## How to run it

Make sure you have Python 3 installed. Then just run:

```
python main.py
```

The program will load any saved data automatically and show you the menu.

## How to use it

When the program starts you will see a menu with numbered options. Type a number and press Enter to choose an option. For example type 1 to register a new customer, type 5 to open an account, type 9 to deposit money. Type 0 when you want to exit and your data will be saved.

## Sample data

There are already some customers and accounts in the data folder so you can test the program straight away without having to create everything from scratch.

## Requirements

Python 3.8 or higher. No extra libraries needed, everything uses the Python standard library.
