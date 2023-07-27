import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QCheckBox, QFormLayout, QDateEdit
from PyQt5.QtCore import Qt, QRegExp, QDate

light_mode_stylesheet = """
    QWidget {
        background-color: #f2f2f2;
        font-family: Arial, sans-serif;
    }

    QLabel {
        color: #333333;
        font-size: 14px;
        font-weight: bold;
    }

    QLineEdit, QTextEdit, QDateEdit {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 5px;
    }

    QPushButton {
        background-color: #4CAF50;
        color: #ffffff;
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
        background-color: #f2f2f2;
        border: none;
    }
"""

light_mode_errorstyle = "background-color: #FFCCCC;"


dark_mode_stylesheet = """
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

dark_mode_errorstyle = "background-color: #CC6666;"


class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):        
        # Create the widgets
        self.num_label = QLabel("Enter a numerical value:")
        self.num_input = QLineEdit()
        
        self.text_label = QLabel("Enter a textual value:")
        self.text_input = QLineEdit()
        
        self.date_label = QLabel("Enter a date (YYYY-MM-DD):")
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        self.output_label = QLabel("Values:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Add a toggle button for dark and light mode
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setChecked(True)  # Set dark mode as the default
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_light_mode)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.print_values)

        # Set the custom validation functions for numeric, text, and date fields
        self.num_input.textChanged.connect(self.validate_numeric)
        self.text_input.textChanged.connect(self.validate_text)
        
        # Create the layout and add widgets
        layout = QFormLayout()
        layout.addRow(self.num_label, self.num_input)
        layout.addRow(self.text_label, self.text_input)
        layout.addRow(self.date_label, self.date_input)
        layout.addRow(self.dark_mode_checkbox)  # Add the toggle button
        layout.addRow(self.submit_button)
        layout.addRow(self.output_label, self.output_text)

        # Set the main layout for the window
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle("Sleek and Modern PyQt GUI")
        self.setGeometry(100, 100, 400, 300)

        # Apply custom CSS styling (optional - if you want to keep the styling from the previous step)
        self.setStyleSheet(dark_mode_stylesheet)

    def toggle_dark_light_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet(dark_mode_stylesheet)
        else:
            self.setStyleSheet(light_mode_stylesheet)
        self.check_validity()

    def validate_numeric(self, event=None):
        input_text = self.num_input.text()
        try:
            int(input_text)
            self.num_input.setStyleSheet("")  # Reset the background color if validation passes
            return True
        except ValueError:
            if self.dark_mode_checkbox.isChecked():
                self.num_input.setStyleSheet(dark_mode_errorstyle)
            else:
                self.num_input.setStyleSheet(light_mode_errorstyle)
            return False
            
    def validate_text(self, event=None):
        input_text = self.text_input.text()
        if 0 < len(input_text) <= 20:
            self.text_input.setStyleSheet("") # reset background color if validation passes
            return True
        else:
            if self.dark_mode_checkbox.isChecked():
                self.text_input.setStyleSheet(dark_mode_errorstyle)
            else:
                self.text_input.setStyleSheet(light_mode_errorstyle)
            return False
        
    def check_validity(self):
        vnum = self.validate_numeric()
        vtext = self.validate_text()
        return vnum and vtext
    
    def print_values(self):
        validData = self.check_validity()
        if validData:
            numerical_value = self.num_input.text()
            textual_value = self.text_input.text()
            date_value = self.date_input.date().toString("yyyy-MM-dd")

            values_to_print = f"Numerical Value: {numerical_value}\nTextual Value: {textual_value}\nDate: {date_value}"
            self.output_text.setPlainText(values_to_print)
        else:
            self.output_text.setPlainText("Some fields do not have valid input data!")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyGUI()
    window.show()
    sys.exit(app.exec_())

