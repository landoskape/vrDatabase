import getpass
import fileManagement as fm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL

def openSession(database, host='localhost', username='root', password=None, port=3306):
    if password is None: password = getpass.getpass()
    urlObject = URL.create("mysql+mysqlconnector", username=username, password=password, host=host, database=database)
    return create_engine(urlObject)

def getTableColumns(table):
    # Extract information about the table metadata
    tableMetadata = table.__table__
    columnNames = tableMetadata.columns.keys()
    columnFeatures = []
    for column in tableMetadata.columns:
        featureDictionary = {
            'Type': column.type,
            'primary_key': column.primary_key,
            'autoincrement': column.autoincrement,
            'nullable': column.nullable,
            'unique': column.unique,
            'default': column.default,
            'server_default': column.server_default,
        }
        columnFeatures.append(featureDictionary)
    
    return columnNames, columnFeatures





