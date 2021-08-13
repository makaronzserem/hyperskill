import sqlite3  #creating a connection object using sqlite3
import account
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')  #returns a sqlite3. Connection class object
        self.cur = self.conn.cursor()  #needed to execute any operations
        #creating the table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')

    def add_new_account(self, account_instance : account.Account):
        self.cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (account_instance.number, account_instance.pin, account_instance.balance))
        self.conn.commit()  #commit changes to database

    def check_if_exist(self, account_v):
        self.cur.execute("SELECT rowid,* FROM card WHERE number=?", (account_v,))
        rows = self.cur.fetchall()  #results from SELECT are put into the list
        return len(rows) != 0

    def log_in_account(self, account_v, pin_v):
        self.cur.execute("SELECT rowid,* FROM card WHERE number=? AND pin=?", (account_v, pin_v))
        rows = self.cur.fetchall()  #results from SELECT are put into the list
        return len(rows) != 0

    def check_balance(self, account_v):
        self.cur.execute("SELECT balance FROM card WHERE number=?", (account_v,))
        rows = self.cur.fetchall()  #results from SELECT are put into the list
        return rows[0][0]  #check balance option 1 / list

    def check_balance_dic(self, account_v):
        self.cur.execute("SELECT balance FROM card WHERE number=?", (account_v,))
        rows = self.cur.fetchall()  #results from SELECT are put into the list

    def closing(self):
        self.cur.close()
        self.conn.close()

    def close_account(self, account_v):
        self.cur.execute("DELETE FROM card WHERE number=?", (account_v, ))
        self.conn.commit()  #commit changes to database

    def add_income(self, account_v, income):
        self.cur.execute("UPDATE card SET balance=? WHERE number=?", (self.check_balance(account_v)+income, account_v,))
        self.conn.commit()  #commit changes to database

    def do_transfer(self, account_v1, account_v2, money):
        helper = self.check_balance(account_v1)
        if helper >= money:
            self.cur.execute("UPDATE card SET balance=? WHERE number=?", (helper-money, account_v1,))
            self.cur.execute("UPDATE card SET balance=? WHERE number=?", (self.check_balance(account_v2)+money, account_v2,))
            self.conn.commit()  #commit changes to database
            return True
        else:
            return False


        #column_info = self.cur.description
        #print(self.cur.fetchall())
        #result = [{column_info[index][0]:value for index, value in enumerate(rows)} for rows in self.cur.fetchall()]
        #print(result)

