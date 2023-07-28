from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector


engine = create_engine('mysql+mysqlconnector://username:password@hostname:port/database')
Session = sessionmaker(bind=engine)
session = Session()

# Creating a new user
new_user = User(name='John Doe', email='john@example.com', age=30)
session.add(new_user)

# Commit the transaction to insert the user into the database
session.commit()


def connect(database=None, host='localhost', user='root', pw=None):
    if pw is None: pw = getpass.getpass()
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=pw, database=database)
    except Exception as me:
        print(me)
        return None
    return mydb

# function to compare a possible entry with an SQL column
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, Date, Time, DateTime

def validate(possible_entry, sql_column):
    # Dictionary mapping SQLAlchemy types to Python types
    type_mapping = {
        Integer: int,
        String: str,
        Boolean: bool,
        Float: float,
        Text: str,
        Date: str,
        Time: str,
        DateTime: str
        # Add more types as needed
    }

    sql_type = type(sql_column.type)
    python_type = type_mapping.get(sql_type)

    # If the Python type is not found in the mapping, return False (invalid entry)
    if python_type is None:
        return False

    # For DateTime fields, you can handle more specific formats if required
    if python_type is str and isinstance(possible_entry, sql_type):
        return True

    # For numeric fields (Integer, Float)
    if python_type in (int, float):
        return isinstance(possible_entry, python_type)

    # For String fields (String, Text)
    if python_type is str:
        max_length = getattr(sql_column.type, 'length', None)
        if max_length and len(possible_entry) > max_length:
            return False
        return True

    # For Boolean fields
    if python_type is bool:
        return isinstance(possible_entry, python_type)

    return False

def validateFast(possible_entry, sql_column):
    # Dictionary mapping SQLAlchemy types to Python types
    type_mapping = {
        Integer: int,
        String: str,
        Boolean: bool,
        Float: float,
        Text: str,
        Date: str,
        Time: str,
        DateTime: str
        # Add more types as needed
    }

    python_type = sql_column.type.python_type

    # If the Python type is not found in the mapping, return False (invalid entry)
    if python_type is None:
        return False

    # For DateTime fields, you can handle more specific formats if required
    if python_type is str and isinstance(possible_entry, sql_type):
        return True

    # For numeric fields (Integer, Float)
    if python_type in (int, float):
        return isinstance(possible_entry, python_type)

    # For String fields (String, Text)
    if python_type is str:
        max_length = getattr(sql_column.type, 'length', None)
        if max_length and len(possible_entry) > max_length:
            return False
        return True

    # For Boolean fields
    if python_type is bool:
        return isinstance(possible_entry, python_type)

    return False


# Example SQL column objects
id_column = Column(Integer, primary_key=True, autoincrement=True)
name_column = Column(String(50), nullable=False)
numeric_column = Column(Float)
boolean_column = Column(Boolean)
comment_column = Column(Text)
date_column = Column(Date)
time_column = Column(Time)
datetime_column = Column(DateTime)

# Possible entries
entry1 = 123  # Valid for an Integer column
entry2 = "John Doe"  # Valid for a String column
entry3 = 3.14  # Valid for a Float column
entry4 = True  # Valid for a Boolean column
entry5 = "This is a long comment."  # Valid for a Text column
entry6 = "2023-07-17"  # Valid for a Date column (ensure it's in the correct date format)
entry7 = "15:30:00"  # Valid for a Time column (ensure it's in the correct time format)

# Validate the entries
print(validate(entry1, id_column))  # Output: True
print(validate(entry2, name_column))  # Output: True
print(validate(entry3, numeric_column))  # Output: True
print(validate(entry4, boolean_column))  # Output: True
print(validate(entry5, comment_column))  # Output: True
print(validate(entry6, date_column))  # Output: True
print(validate(entry7, time_column))  # Output: True
print(validate(entry6 + " " + entry7, datetime_column))  # Output: True (for combined date and time)




"""
# This is a yaml file that provides the details of the "sessions" table for a MySQL database
# ATL230728 - Note to self: the possible "features" of a column are: 
#           - field, type, collation, null, key, default, extra, privileges, comment
---
tableName: sessions
columnNames:
  - name: unique identifier
    type: INTEGER
    primary_key: true
    auto_increment: true
  - name: mouse name
    type: VARCHAR
    length: 50
    not_null: true
  - name: date
    type: VARCHAR
  - name: age
    type: INTEGER
  - name: created_at
    type: TIMESTAMP
    default: CURRENT_TIMESTAMP




unique identifier
mouseName
date
session ID
unique mouse ID
experiment type
imaging
face camera
vrEnvironments
number of imaging planes
separation of imaging planes
pockels cell percentage
rotation of objective
rotation of head plate holder
suite2p processed
suite2p quality control
vrExperiment registration processed
red cell quality control
session quality control

"""