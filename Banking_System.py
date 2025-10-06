import json
import os

# File to store account data
ACCOUNTS_FILE = "bank_accounts.json"

def load_accounts():
    """Load accounts from JSON file"""
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_accounts(accounts):
    """Save accounts to JSON file"""
    try:
        with open(ACCOUNTS_FILE, 'w') as file:
            json.dump(accounts, file, indent=4)
    except IOError:
        print("Error: Could not save account data!")

def open_new_account(accounts):
    """Open a new bank account"""
    print("\n--- Open New Account ---")
    
    account_number = input("Enter new account number: ")
    
    if account_number in accounts:
        print("Error: Account number already exists!")
        return
    
    name = input("Enter account holder name: ")
    
    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount: "))
            if initial_deposit < 0:
                print("Error: Initial deposit cannot be negative!")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number!")
    
    # Create new account
    accounts[account_number] = {
        'name': name,
        'balance': initial_deposit,
        'transactions': [f"Initial deposit: ${initial_deposit:.2f}"]
    }
    
    save_accounts(accounts)
    print(f"\nAccount created successfully!")
    print(f"Account Number: {account_number}")
    print(f"Account Holder: {name}")
    print(f"Initial Balance: ${initial_deposit:.2f}")

def existing_account_operations(accounts):
    """Handle operations for existing accounts"""
    print("\n--- Existing Account ---")
    
    account_number = input("Enter your account number: ")
    
    if account_number not in accounts:
        print("Error: Account not found!")
        return
    
    account = accounts[account_number]
    print(f"\nWelcome {account['name']}!")
    print(f"Current Balance: ${account['balance']:.2f}")
    
    while True:
        print("\n1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Transaction History")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            print(f"\nCurrent Balance: ${account['balance']:.2f}")
        
        elif choice == '2':
            deposit_amount = get_valid_amount("Enter deposit amount: ")
            if deposit_amount > 0:
                account['balance'] += deposit_amount
                account['transactions'].append(f"Deposit: ${deposit_amount:.2f}")
                save_accounts(accounts)
                print(f"\nDeposit successful! New balance: ${account['balance']:.2f}")
            else:
                print("Error: Deposit amount must be positive!")
        
        elif choice == '3':
            withdraw_amount = get_valid_amount("Enter withdrawal amount: ")
            if withdraw_amount > 0:
                if withdraw_amount <= account['balance']:
                    account['balance'] -= withdraw_amount
                    account['transactions'].append(f"Withdrawal: ${withdraw_amount:.2f}")
                    save_accounts(accounts)
                    print(f"\nWithdrawal successful! New balance: ${account['balance']:.2f}")
                else:
                    print("Error: Insufficient funds!")
            else:
                print("Error: Withdrawal amount must be positive!")
        
        elif choice == '4':
            print("\n--- Transaction History ---")
            if account['transactions']:
                for transaction in account['transactions']:
                    print(transaction)
            else:
                print("No transactions yet.")
            print(f"Current Balance: ${account['balance']:.2f}")
        
        elif choice == '5':
            break
        
        else:
            print("Error: Invalid choice! Please enter 1-5.")

def get_valid_amount(prompt):
    """Get a valid positive amount from user"""
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                print("Error: Amount cannot be negative!")
                continue
            return amount
        except ValueError:
            print("Error: Please enter a valid number!")

def display_all_accounts(accounts):
    """Display all accounts (admin function)"""
    print("\n--- All Accounts ---")
    if not accounts:
        print("No accounts found.")
        return
    
    for acc_num, details in accounts.items():
        print(f"Account: {acc_num}, Holder: {details['name']}, Balance: ${details['balance']:.2f}")

def main():
    """Main banking system function"""
    print("=== Welcome to Python Banking System ===")
    
    # Load existing accounts
    accounts = load_accounts()
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Open New Account")
        print("2. Existing Account")
        print("3. Display All Accounts (Admin)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            open_new_account(accounts)
        
        elif choice == '2':
            existing_account_operations(accounts)
        
        elif choice == '3':
            display_all_accounts(accounts)
        
        elif choice == '4':
            print("\nThank you for using our banking system!")
            break
        
        else:
            print("Error: Invalid choice! Please enter 1-4.")

if __name__ == "__main__":
    main()