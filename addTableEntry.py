import sys
import importlib
from functools import partial
import databaseManagement as dm
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QCheckBox, QFormLayout, QDateEdit
from PyQt5.QtCore import Qt, QRegExp, QDate

# handle input arguments
n = len(sys.argv)
assert n==2, "the only input argument should be the name of the table you want to add data to!"

# get table name and import the table
tableName = sys.argv[1]
module = importlib.import_module('tables')
table = getattr(module, tableName, None)

# make sure it all worked as expected
if table is None: 
    raise ValueError(f"{tableName} was not found in the tables.py module!")
try:
    columnNames, columnFeatures = dm.getTableInfo(table)
except Exception as ex:
    raise ValueError(f"The table you requested {tableName} is probably not a valid table object.")

def addElement(engine, newRow):
    print('add element, in addTableEntry, needs to be coded (along with some supporting functions)')
    # with Session(engine) as session:
    #     session.add(newRow)
    #     session.commit()
    return None

# prepare GUI
darkModeStylesheet = """
    QWidget {
        background-color: #1F1F1F;
        color: #F0F0F0;
        font-family: Arial, sans-serif;
    }

    QLabel {
        color: #E0E0E0;
        font-size: 14px;
        font-weight: bold;
    }

    QLineEdit, QTextEdit, QDateEdit {
        background-color: #333333;
        color: #F0F0F0;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 5px;
    }

    QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
        border: 1px solid #7F7F7F;
    }

    QPushButton {
        background-color: #4CAF50;
        color: #F0F0F0;
        font-size: 14px;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }

    QPushButton:hover {
        background-color: #45a049;
        font-size: 14px;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }

    QTextEdit[readOnly="true"] {
        background-color: #1F1F1F;
        border: none;
    }
"""

darkModeErrorStyle = "background-color: #CC6666;"


class MyGUI(QWidget):
    def __init__(self, columnNames):
        super().__init__()
        self.init_ui(columnNames)

    def init_ui(self, columnNames):
        assert isinstance(columnNames, list), "columnNames must be a list"
        assert all([isinstance(col, str) for col in columnNames]), "columnNames must be strings"
        
        # For each column name, create a label and an edit field
        self.columnNames = columnNames
        self.numColumns = len(self.columnNames)
        self.columnLabels = []
        self.columnEntries = []
        for colName in self.columnNames:
            self.columnLabels.append(QLabel(f"{colName}:"))
            self.columnEntries.append(QLineEdit())
            
        # Create a display area to print the full entry
        self.outputLabel = QLabel("New Entry:")
        self.outputEntry = QTextEdit()
        self.outputEntry.setReadOnly(True)
        
        # Create a button for submitting the new entry to a table
        self.submitEntry = QPushButton("Submit")
        self.submitEntry.clicked.connect(self.printValues)
        
        # Set validation functions for each field
        for idx,inputs in enumerate(self.columnEntries):
            inputs.textChanged.connect(partial(self.validateInput, columnIndex=idx))
        
        # Create the layout and add widgets
        layout = QFormLayout()
        for label,entry in zip(self.columnLabels, self.columnEntries):
            layout.addRow(label, entry)
        layout.addRow(self.submitEntry)
        layout.addRow(self.outputLabel, self.outputEntry)

        # Set the main layout for the window
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle("Add Entry to Database")
        self.setGeometry(100, 100, 400, 300)

        # Apply custom CSS styling (optional - if you want to keep the styling from the previous step)
        self.setStyleSheet(darkModeStylesheet)

    def validateInput(self, event=None, columnIndex=None):
        if 0 < len(self.columnEntries[columnIndex].text()) <= 20:
            self.columnEntries[columnIndex].setStyleSheet("")
            return True
        else: 
            self.columnEntries[columnIndex].setStyleSheet(darkModeErrorStyle)
            return False
        
    def checkValidity(self):
        validEntries = [self.validateInput(columnIndex=idx) for idx in range(self.numColumns)]
        return all(validEntries)
    
    def printValues(self):
        validData = self.checkValidity()
        if validData:
            stringToPrint = ""
            for colName, colEntry in zip(self.columnNames, self.columnEntries):
                stringToPrint += f"{colName}: {colEntry.text()}\n"
            self.outputEntry.setPlainText(stringToPrint)
        else:
            self.outputEntry.setPlainText("Some fields do not have valid input data!")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyGUI(columnNames)
    window.show()
    sys.exit(app.exec_())

