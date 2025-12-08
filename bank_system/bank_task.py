accounts = {}     # Stores user accounts and balance

# Create or Update Account - Deposit 
def deposit():
    name = input("\nEnter your name: ").lower()
    amount = int(input("Enter amount to deposit: "))

    # If user exists, update balance, Else create account.
    accounts[name] = accounts.get(name, 0) + amount

    print(f"\nSUCCESS: Amount Deposited Successfully for {name}")
    print("Current Balance:", accounts[name])

# Withdraw Function 
def withdraw():
    name = input("\nEnter your name for withdrawal: ").lower()

    if name not in accounts:
        print("\nERROR: Account not found! Please deposit first to create account.")
        return

    withdraw_amount = int(input("Enter amount to withdraw: "))

    current_balance = accounts[name]

    # cannot withdraw more than balance
    if withdraw_amount > current_balance:
        print("\nERROR: Unable to withdraw — Insufficient Balance")
        return

    accounts[name] = current_balance - withdraw_amount
    print("\nSUCCESS: Withdrawal successful")
    print("Balance Amount:", accounts[name])

# Show Balance
def show_balance():
    name = input("\nEnter your name: ").lower()

    if name in accounts:
        print("\nCurrent Balance for", name, ":", accounts[name])
    else:
        print("\nERROR: No account found! Please deposit first.")

# Show All Accounts
def show_all_accounts():
    if not accounts:
        print("\nERROR: No accounts available.")
        return

    print("\n----- All Accounts -----")
    for user, bal in accounts.items():
        print(user.capitalize(), "→", bal)

# MAIN MENU
while True:
    print("\n===== BANK MENU =====\n")
    print("1. Deposit Amount")
    print("2. Withdraw Amount")
    print("3. Show Balance")
    print("4. Show All Accounts")
    print("5. Exit")

    choice = int(input("Enter your choice (1-5): "))

    if choice == 1:
        deposit()
    elif choice == 2:
        withdraw()
    elif choice == 3:
        show_balance()
    elif choice == 4:
        show_all_accounts()
    elif choice == 5:
        print("\nThank you!")
        break
    else:
        print("\nERROR: Invalid choice! Please enter 1-5\n")
