class Account:
    def __init__(self, account_number, owner_name, balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance
        self.left = None
        self.right = None


def insert_account(root, account_number, owner_name, balance):
    if root is None:  # checks if the current tree is empty
        return Account(account_number, owner_name, balance)
    if account_number < root.account_number:  # If the new account number is less than the current node’s account number,the function recursively calls itself on the left child
        root.left = insert_account(root.left, account_number, owner_name, balance)
    elif account_number > root.account_number:
        root.right = insert_account(root.right, account_number, owner_name, balance)
    else:
        print(f"Account with number {account_number} already exists.")
    return root


def search_account(root, account_number):
    if root is None:
        return None  # Account not found


    if account_number == root.account_number:
        return root

    elif account_number < root.account_number:
        # Search in the left subtree
        return search_account(root.left, account_number)

    else:
        # Search in the right subtree
        return search_account(root.right, account_number)



deposit_queue = []  # Queue to hold pending deposit transactions


def enqueue_deposit(account_number, amount):
    deposit_queue.append({'account_number': account_number, 'amount': amount})  # Add deposit request to queue
    print(f"Deposit request queued for account {account_number}, amount {amount}")


def process_deposits(root):
    while deposit_queue:
        txn = deposit_queue.pop(0)  # Remove first transaction from queue (FIFO)
        account = search_account(root, txn['account_number'])  # Find account in BST
        if account:
            account.balance += txn['amount']  # Update account balance
            print(
                f"Processed deposit: {txn['amount']} to account {txn['account_number']}. New balance: {account.balance}")
        else:
            print(f"Account {txn['account_number']} not found.")  # Handle missing account


# Global queue to hold withdrawal transactions
withdrawal_queue = []


def enqueue_withdraw(account_number, amount):  # Adds a withdrawal request to the withdrawal queue.
    withdrawal_queue.append({'account_number': account_number, 'amount': amount})
    print(f"Withdrawal request queued for account {account_number}, amount {amount}")


def process_withdrawals(root):
    while withdrawal_queue:
        txn = withdrawal_queue.pop(0)  # Dequeue the first transaction
        # Find account in BST
        account = search_account(root, txn['account_number'])

        if account:
            # Check if there are sufficient funds
            if account.balance >= txn['amount']:
                account.balance -= txn['amount']  # Deduct amount from balance
                print(
                    f"Processed withdrawal: {txn['amount']} from account {txn['account_number']}. New balance: {account.balance}")
            else:
                print(
                    f"Insufficient funds for withdrawal from account {txn['account_number']}. Current balance: {account.balance}")
        else:
            print(f"Account {txn['account_number']} not found.")


transfer_queue = []


def enqueue_transfer(main_account_number, dest_account_number, amount):
    transfer_queue.append({
        'source_account': main_account_number,
        'dest_account': dest_account_number,
        'amount': amount
    })
    print(f"Transfer request queued: {amount} from account {main_account_number} to account {dest_account_number}")


def process_transfers(root):
    while transfer_queue:
        txn = transfer_queue.pop(0)  # Dequeue the first transaction
        main_account = search_account(root, txn['main_account'])
        dest_account = search_account(root, txn['dest_account'])

        if main_account and dest_account:
            if main_account.balance >= txn['amount']:
                main_account.balance -= txn['amount']
                dest_account.balance += txn['amount']
                print(f"Transferred {txn['amount']} from {txn['main_account']} to {txn['dest_account']}")
            else:
                print(f"Insufficient funds for transfer from account {txn['main_account']}")
        else:
            if not main_account:
                print(f"main account {txn['main_account']} not found")
            if not dest_account:
                print(f"Destination account {txn['dest_account']} not found")


def delete_account(root, account_number):
    if root is None:
        return root

    if account_number < root.account_number:
        root.left = delete_account(root.left, account_number)
    elif account_number > root.account_number:
        root.right = delete_account(root.right, account_number)
    else:
        # Node found, perform deletion

        # Case 1: No child
        if root.left is None and root.right is None:
            return None

        # Case 2: One child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Case 3: Two children
        # Find inorder successor (smallest in right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left

        # Replace root data with successor data
        root.account_number = successor.account_number
        root.owner_name = successor.owner_name
        root.balance = successor.balance

        # Delete successor node
        root.right = delete_account(root.right, successor.account_number)

    return root


def report_account_balance(root, account_number): # Searches for the account by account_number in the BST and  reports the balance and account details
    account = search_account(root, account_number)  # Uses the existing search function

    if account:
        print(f"Account Number: {account.account_number}")
        print(f"Owner Name: {account.owner_name}")
        print(f"Current Balance: {account.balance}")
    else:
        print(f"Account {account_number} not found.")


def search_For_accounts_In_Balance(root, min_balance, max_balance):
    if root is None:
        return

    search_For_accounts_In_Balance(root.left, min_balance, max_balance)  # Traverse left subtree (all accounts with smaller account numbers)

    if min_balance <= root.balance <= max_balance:    # Check if the current account balance is in the desired range
        print(f"Account Number: {root.account_number}, Owner: {root.owner_name}, Balance: {root.balance}")

    search_For_accounts_In_Balance(root.right, min_balance, max_balance)  # Traverse right subtree (all accounts with larger account numbers)


def main():
    root = None  # Starts with empty BST

    while True:
        print("\n--- Bank Management System ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Process Deposits")
        print("6. Process Withdrawals")
        print("7. Process Transfers")
        print("8. Report Account Balance")
        print("9. Search Accounts by Balance Range")
        print("10. Delete Account")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            acc_num = int(input("Enter account number: "))
            name = input("Enter owner name: ")
            bal = float(input("Enter initial balance: "))
            root = insert_account(root, acc_num, name, bal)
            print("Account created successfully.")

        elif choice == '2':
            acc_num = int(input("Enter account number for deposit: "))
            amount = float(input("Enter deposit amount: "))
            enqueue_deposit(acc_num, amount)

        elif choice == '3':
            acc_num = int(input("Enter account number for withdrawal: "))
            amount = float(input("Enter withdrawal amount: "))
            enqueue_withdraw(acc_num, amount)

        elif choice == '4':
            source_acc = int(input("Enter source account number: "))
            dest_acc = int(input("Enter destination account number: "))
            amount = float(input("Enter amount to transfer: "))
            enqueue_transfer(source_acc, dest_acc, amount)

        elif choice == '5':
            print("Processing deposit transactions...")
            process_deposits(root)

        elif choice == '6':
            print("Processing withdrawal transactions...")
            process_withdrawals(root)

        elif choice == '7':
            print("Processing transfer transactions...")
            process_transfers(root)

        elif choice == '8':
            acc_num = int(input("Enter account number to report balance: "))
            report_account_balance(root, acc_num)

        elif choice == '9':
            min_bal = float(input("Enter minimum balance: "))
            max_bal = float(input("Enter maximum balance: "))
            print(f"Accounts with balance between {min_bal} and {max_bal}:")
            search_For_accounts_In_Balance(root, min_bal, max_bal)

        elif choice == '10':
            acc_num = int(input("Enter account number to delete: "))
            root = delete_account(root, acc_num)
            print(f"Account {acc_num} deleted if existed.")

        elif choice == '0':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()



