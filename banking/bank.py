from account import Account
import random
import sql

class Bank:
    def __init__(self,db_conn : sql.Database):
        self.db_connection = db_conn

    def create_account(self):
        while True:
            prefix = "400000"
            inefix = str(random.randint(100000000, 999999999))
            account_num = prefix + inefix  #15 digits

            #algorithm Luhna
            copy_account = []
            for j in range(0, 15):
                copy_account.append(account_num[j])
            copy_account = [int(n) for n in copy_account]
            for i in range(0, 15):
                if i % 2 == 0:
                    copy_account[i] =  copy_account[i] * 2
            for i in range(0, 15):
                if copy_account[i] > 9:
                    copy_account[i] =  copy_account[i] - 9
            sum_num = 0
            for i in range(0, 15):
                sum_num += copy_account[i]

            if sum_num % 10 == 0:
                checksum = 0
            else:
                y = sum_num // 10
                checksum = (y + 1) * 10 - sum_num
            account_num = prefix + inefix + str(checksum)

            if not self.db_connection.check_if_exist(account_num):
                new_pin = random.randint(1000, 9999)
                new_account = Account(account_num, new_pin)
                #self.accounts[account_num] = new_account
                self.db_connection.add_new_account(new_account)
                print("Your card has been created")
                print("Your card number:")
                print(account_num)
                print("Your card PIN:")
                print(new_pin)
                break


    def log_in(self):
        print("Enter your card number:")
        card_numb = int(input())
        print("Enter your PIN:")
        login_pin = int(input())

        if self.db_connection.log_in_account(card_numb, login_pin):
            print("You have successfully logged in!")
            self.menu_logged(card_numb)
        else:
            print("Wrong card number or PIN!")

    def log_out(self):
        print("You have successfully logged out!")

    def menu(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            choice = int(input())

            if choice == 0:
                print("Bye")
                self.db_connection.closing()
                exit()
            elif choice == 1:
                self.create_account()
            elif choice == 2:
                self.log_in()

    def menu_logged(self, card_num):
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")
        choice = int(input())

        if choice == 0:
            print("Bye")
            exit()
        elif choice == 1:
            print(self.db_connection.check_balance(card_num))
        elif choice == 2:
            self.log_out()
