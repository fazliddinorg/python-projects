def show_balance(balance):
    """
    Display the current balance.

    Parameters:
    balance (float): The current balance in the account.
    """
    print(f"Your balance is ${balance:.2f}")


def deposit():
    """
    Prompt the user to enter an amount to deposit.

    Returns:
    float: The amount to be deposited if valid, otherwise 0.
    """
    try:
        amount = float(input("Enter an amount to be deposited: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return 0
        else:
            return amount
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return 0


def withdraw(balance):
    """
    Prompt the user to enter an amount to withdraw.

    Parameters:
    balance (float): The current balance in the account.

    Returns:
    float: The amount to be withdrawn if valid, otherwise 0.
    """
    try:
        amount = float(input("Enter an amount to withdraw: "))
        if amount > balance:
            print("Insufficient funds.")
            return 0
        elif amount <= 0:
            print("Amount must be greater than 0.")
            return 0
        else:
            return amount
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return 0


def show_transaction_history(transaction_history):
    """
    Display the transaction history.

    Parameters:
    transaction_history (list): A list of transaction records.
    """
    if not transaction_history:
        print("No transactions to show.")
    else:
        for transaction in transaction_history:
            print(transaction)


def main():
    """
    Main function to run the banking program.
    """
    balance = 0
    transaction_history = []
    is_running = True

    account_holder = input("Enter account holder's name: ")
    print(f"Welcome, {account_holder}!")

    while is_running:
        print("\nBanking Program")
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Show Transaction History")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            show_balance(balance)
        elif choice == "2":
            amount = deposit()
            if amount > 0:
                balance += amount
                transaction_history.append(f"Deposited: ${amount:.2f}")
        elif choice == "3":
            amount = withdraw(balance)
            if amount > 0:
                balance -= amount
                transaction_history.append(f"Withdrew: ${amount:.2f}")
        elif choice == "4":
            show_transaction_history(transaction_history)
        elif choice == "5":
            is_running = False
        else:
            print("That is not a valid choice!")

    print(f"Thank you, {account_holder}! Have a nice day!")


if __name__ == "__main__":
    main()