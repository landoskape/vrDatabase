import getpass
import fileManagement as fm

from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, DBAPIError
from sqlalchemy_utils.functions import database_exists

def createEngine(database=None, host='localhost', username='root', password=None, port=3306, dialectDriver='mysql+mysqlconnector'):
    if database is None: database = input("Database: ")
    if password is None: password = getpass.getpass(prompt="Password: ")
    urlObject = URL.create(dialectDriver, username=username, password=password, host=host, database=database)
    # first check if databaseExists. This will raise an error if anything is wrong (e.g. password issues)
    # or it will report True/False if everything else is good and just inform about the database existing 
    try:
        databaseExists = database_exists(urlObject)
    except Exception as exc:
        print(exc)
        return None
    # either tell the user the database doesn't exist and return none, or give them an engine to work with
    if not(databaseExists): 
        print(f"Requested database: {database} does not exist!")
        return None
    else:
        return create_engine(urlObject)
    
def getTableInfo(table):
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

def requiresUserInfo(columnFeatures):
    # for a dictionary describing the column features (see "getTableInfo()"), this determines whether this column requires user info to add an entry to a table...
    requiresInfo = []
    for features in columnFeatures:
        if features["autoincrement"]==True:
            requiresInfo.append(False)
        elif features["server_default"] is not None:
            requiresInfo.append(False)
        else:
            requiresInfo.append(True)
    return requiresInfo

def validateInput(inputText, columnFeatures):
    return True




