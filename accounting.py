#!/bin/python

import sys
import sqlite3 as lite

def main():
    """Run the accounting View and Controller"""
    print('Simple python accounting program')
    conn = input("Enter name of book to open (or create if does not exit): ")
    try:
        db = lite.connect(conn)
        c = db.cursor()
        c.execute('''CREATE TABLE debits (id INTEGER UNIQUE PRIMARY KEY, date TEXT, desc TEXT, amount INTEGER)''')
        c.execute('''CREATE TABLE credits (id INTEGER UNIQUE PRIMARY KEY, date TEXT, desc TEXT, amount INTEGER)''')
    except lite.Error as e:
        print("Error %s" % e.args[0])
    print_menu() 
    s = input("Select 1-5 or q: ")
    while s != 'q':
        parse_menu(c, s)
        db.commit()
        print_menu()
        s = input("select 1-5 or q: ")
    return

def print_menu():
    """Print a simple menu of options"""
    print("""Select options:
        1:  Print ledger
        2:  Add credit
        3:  Add debit
        4:  Delete credit
        5:  Delete debit
        0:  Change database
        q:  Quit""")
    return

def parse_menu(c, s):
    """Handle menu selections"""
    if s == '0':
        pass
    if s == '1':
        print_ledger(c)
    if s == '2':
        add_credit(c, get_entry())
    if s == '3':
        add_debit(c, get_entry())
    if s == '4':
        del_credit(c, get_deletion())
    if s == '5':
        del_debit(c, get_deletion())
    if s == '0':
        new_db = input("Enter name of book: ")
        db = lite.connect(new_db)
    return

def get_entry():
    """Collect info for entry as DB or CR
       and return as a tuple"""
    date = input("Enter date of transaction: ")
    desc = input("Enter a description: ")
    amt = input("Enter the amount of the transaction: ")
    return (date, desc, amt)

def get_deletion():
    """Collect info about which entry to delete
       and return as a tuple"""
    print("Enter as much info as available about item to delete.")
    item = input("Enter item number of transaction: ")
    date = input("Enter date of transaction: ")
    desc = input("Enter a description: ")
    amt = input("Enter the amount of the transaction: ")
    return (item, date, desc, amt)
 
def print_ledger(c):
    """Prints out the double entry ledger"""
    print("Credits")
    for row in c.execute("SELECT * FROM credits"):
        print(row)
    print("Debits")
    for row in c.execute("SELECT * FROM debits"):
        print (row)
    print(c.fetchone())
    return

def add_debit(c, entry):
    """Add entry to debit book"""
    c.execute('INSERT INTO debits(date,desc,amount) VALUES(?, ?, ?)', entry)
    print("Entry added for %s  %s  %s." % entry)
    return 

def add_credit(c, entry):
    """Add entry to credit book"""
    date, desc, amt = entry
    c.execute('INSERT INTO credits(date,desc,amount) VALUES(?, ?, ?)', (date, desc, amt))
    print("Entry added for %s  %s  %s." % entry)
    return

def del_debit(c, entry):
    """Delete an entry from debit book"""
    item, date, desc, amt = entry
    if item:
        c.execute('DELETE FROM debits WHERE id=?', item)
    return

def del_credit(c, entry):
    """Delete an entry from the credit book"""
    item, date, desc, amt = entry
    if item:
        c.execute('SELECT * FROM credits WHERE id=?', item)
        print('Are you sure you want to delete the following?')
        print(c.fetchone())
        if input('y or N') == 'y':
            c.execute('DELETE FROM credits WHERE id=?', item)
            return True
        else:
            return False
    print('\nYour criteria matched the following entries:')
    for row in c.execute('SELECT * FROM credits WHERE date=? OR desc=? OR amount=?', (date, desc, amt)):
        print(row)
    i = input('\nEnter item number to delete: ')
    if i:
        if c.execute('SELECT * FROM credits WHERE id=?', i):
            s = c.fetchone()
            if input('Are you sure you want to delete %s? (y or N): ') == 'y':
                c.execute('DELETE FROM credits WHERE id=?', i)
                return True
            else:
                return False
    return

if __name__ == '__main__':
    status = main()
    sys.exit(status)
