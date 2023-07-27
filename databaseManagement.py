import getpass
import mysql.connector


def connect(database=None, host='localhost', user='root', pw=None):
    if pw is None: pw = getpass.getpass()
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=pw, database=database)
    except Exception as me:
        print(me)
        return None
    return mydb
