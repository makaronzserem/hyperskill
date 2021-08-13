from sql import Database
from bank import Bank
db = Database()
start = Bank(db)
start.menu()
