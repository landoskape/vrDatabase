import mysql.connector

def connect(database, host='localhost', user='root', pw=None):
    mydb = mysql.connector.connect(host=host, user=user, password=pw, database=database)
    return mydb
