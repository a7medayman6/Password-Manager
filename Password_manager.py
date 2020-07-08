import base64
import sqlite3
from sqlite3 import Error

def connect(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)    
    return conn

def create_table(cur, table_name):
    sql_cmd = """CREATE TABLE IF NOT EXISTS {table_name}
        (
            name text,
            password text

        ); """.format(table_name = table_name)
    cur.execute(sql_cmd)
    
def select_all(cur, table_name):
    sql_cmd = """SELECT rowid, name from {table_name}""".format(table_name = table_name)
    cur.execute(sql_cmd)
    rows = cur.fetchall()

    return rows
def select_row(cur, table_name, id):
    sql_cmd = """SELECT * from {table_name} WHERE rowid = ?""".format(table_name = table_name)
    cur.execute(sql_cmd, id)
    rows = cur.fetchall()

    return rows
def insert_service(cur, table_name, name, password):
    sql_cmd = """INSERT INTO {table_name}
        (name, password)    
        VALUES(?, ?)""".format(table_name = table_name)
    service = name, password    
    cur.execute(sql_cmd, service)
    print("Service Added Successfully.\n")

def delete_service(cur, table_name, id):
    sql_cmd = """DELETE FROM {table_name} WHERE rowid = ?""".format(table_name = table_name)
    cur.execute(sql_cmd, id)
    print("Service Deleted Successfully.\n")

def update_service(cur, table_name, id, name, password):
    sql_cmd = """UPDATE {table_name} SET name = ?, password = ? WHERE rowid = ?""".format(table_name = table_name)
    service = name, password, id
    cur.execute(sql_cmd, service)
    print("Service Updated Successfully.\n")


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def print_rows(rows):
    print("\nid\tservice\n")
    for row in rows:
        for element in row:
            print(element, "\t", end="")
        print()     


master_password = "cGFzc3dvcmQ=" #base64 encoding for 'password'
master_pass = input("Enter the master password:\t")

while master_pass != base64.b64decode(master_password).decode('utf-8'):
    print("WRONG PASSWORD.\n")
    master_pass = input("Enter the master password:\t")

DB_NAME = "manager.db"
TABLE_NAME = "service"

CONN = connect(DB_NAME)
if CONN is not None:

    CUR = CONN.cursor()
    create_table(CUR, TABLE_NAME)
    commands_pallate = "\n\tCOMMANDS.\n:q = Quite the program.\n:add = Add a new service.\n:get = Get a service password.\n:del = Delete a service.\n:update = Update a service.\n"
    print(commands_pallate)
    choice = input(":")
    while choice != 'q':

        if choice == 'add':
            s_name = input("Service Name:\t")
            s_pass = input("Service Password:\t")
            insert_service(CUR, TABLE_NAME, s_name, s_pass)
            CONN.commit()
        elif choice == 'get':
            ROWS = select_all(CUR, TABLE_NAME)
            if len(ROWS) != 0:
                print_rows(ROWS)
                id = input("Choose the service id:\t")
                while not is_integer(id):
                    print("ERROR: id must be integer.\n")
                    id = input("Choose the service id:\t")
                ROWS = select_row(CUR, TABLE_NAME, id)
                if len(ROWS) != 0:
                    print_rows(ROWS)
                else:
                    print("There is no services added.") 

                CONN.commit()
            else:
                print("There is no services added.")

        elif choice == 'del':
            ROWS = select_all(CUR, TABLE_NAME)
            if len(ROWS) != 0:
                print_rows(ROWS)
                id = input("Choose the service id:\t")
                while not is_integer(id):
                    print("ERROR: id must be integer")
                    id = input("Choose the service id:\t")
                delete_service(CUR, TABLE_NAME, id)
                CONN.commit()
            else:
                print("There is no services added.")    

        elif choice == 'update':

            ROWS = select_all(CUR, TABLE_NAME)
            if len(ROWS) != 0:
                print_rows(ROWS)
                id = input("Choose the service id:\t")
                while not is_integer(id):
                    print("ERROR: id must be integer")
                    id = input("Choose the service id:\t")
                s_name = input("Service Name:\t")
                s_pass = input("Service Password:\t")    
                update_service(CUR, TABLE_NAME, id, s_name, s_pass)
                CONN.commit()
            else:
                print("There is no services added.") 
        else:
            print("Wrong Choice.\n")

        print(commands_pallate)
        choice = input(":")

else:
    print("ERROR!")    


CONN.close()    