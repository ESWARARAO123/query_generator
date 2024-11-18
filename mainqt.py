import sys
import re
import csv
from sqlalchemy import create_engine, inspect, text
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QHBoxLayout, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# Database connection setup
engine = create_engine("postgresql+psycopg2://postgres:root@localhost/demo")


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Query Chat")
        self.setGeometry(100, 100, 800, 600)

        # Apply a stylesheet for colors and fonts
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #d1d9e6;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial';
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #4caf50;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial';
            }
            QPushButton {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #4caf50;
                font-size: 16px;
                font-family: 'Arial';
                margin-bottom: 5px;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #d1d9e6;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial';
            }
        """)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        # User input area
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your question here...")
        input_layout.addWidget(self.user_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_query)
        input_layout.addWidget(self.send_button)
        self.layout.addLayout(input_layout)

        # Results table (hidden by default)
        self.results_table = QTableWidget()
        self.results_table.setVisible(False)
        self.layout.addWidget(self.results_table)

        # Download button (hidden by default)
        self.download_button = QPushButton("Download Results")
        self.download_button.setVisible(False)
        self.download_button.clicked.connect(self.download_results)
        self.layout.addWidget(self.download_button)

        # Storage for the results to be downloaded
        self.current_results = []

    def handle_query(self):
        """Handle the user's question input and execute the corresponding SQL query."""
        question = self.user_input.text().strip()
        if not question:
            return

        # Display user input in the chat
        self.append_to_chat("You", question, "#4caf50")

        sql_query, results = self.generate_sql_query(question)

        # Display SQL query and results in the chat
        if sql_query:
            self.append_to_chat("System", f"Generated SQL Query:\n{sql_query}", "#d32f2f")
        if results:
            if isinstance(results, list) and results:
                self.current_results = results
                self.display_results_in_table(results)
                self.results_table.setVisible(True)

                # Show the download button if results have more than one row or column
                if len(results) > 1 or (len(results) == 1 and len(results[0]) > 1):
                    self.download_button.setVisible(True)
                else:
                    self.download_button.setVisible(False)
            else:
                self.append_to_chat("System", "No results found.", "#1976d2")
                self.results_table.setVisible(False)
                self.download_button.setVisible(False)
        else:
            self.append_to_chat("System", "No results found.", "#1976d2")
            self.results_table.setVisible(False)
            self.download_button.setVisible(False)

        # Clear the input field
        self.user_input.clear()

    def append_to_chat(self, sender, message, color):
        """Append a styled message to the chat display."""
        self.chat_display.append(f"<b style='color:{color}'>{sender}:</b> {message}\n")
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def display_results_in_table(self, results):
        """Display the query results in a table format."""
        if not results:
            return

        self.results_table.clear()
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(results[0]))
        self.results_table.setHorizontalHeaderLabels(results[0].keys())

        for row_idx, row_data in enumerate(results):
            for col_idx, (col_name, col_value) in enumerate(row_data.items()):
                item = QTableWidgetItem(str(col_value))
                self.results_table.setItem(row_idx, col_idx, item)

        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def download_results(self):
        """Download the current query results as a CSV file."""
        if not self.current_results:
            return

        # Open a file dialog to save the CSV file
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Save Results", "results.csv", "CSV Files (*.csv)")

        if file_path:
            try:
                # Write the results to the file
                with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=self.current_results[0].keys())
                    writer.writeheader()
                    writer.writerows(self.current_results)
                QMessageBox.information(self, "Success", "Results successfully saved!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")

    def get_all_tables(self):
        """Retrieve all table names in the database."""
        inspector = inspect(engine)
        return inspector.get_table_names()

    def get_columns_from_table(self, table_name):
        """Get the column names of a specified table."""
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        return [column["name"] for column in columns]

    def execute_sql_query(self, query):
        """Execute the generated SQL query on the database and return the results."""
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            return [{"Error": str(e)}]

    def match_table_and_column(self, question):
        """Identify the relevant table and column based on the question content."""
        all_tables = self.get_all_tables()
        selected_table = None
        selected_column = None

        # Match table
        for table in all_tables:
            if f" {table.lower()} " in f" {question} ":
                selected_table = table
                break

        if not selected_table:
            for table in all_tables:
                if table.lower() in question:
                    selected_table = table
                    break

        if selected_table:
            columns = self.get_columns_from_table(selected_table)
            for column in columns:
                if column.lower() in question:
                    selected_column = column
                    break
            return selected_table, selected_column

        for table in all_tables:
            columns = self.get_columns_from_table(table)
            for column in columns:
                if column.lower() in question:
                    return table, column

        return None, None

    def generate_sql_query(self, question):
        """Generate SQL query based on the user's question."""
        question = question.lower()
        selected_table, selected_column = self.match_table_and_column(question)

        if not selected_table:
            return "SELECT 'No matching table found in the database.';", []
        if not selected_column:
            return f"SELECT 'Table {selected_table} found, but no matching column identified.';", []

    # Handle range queries: "between X and Y"
        range_match = re.search(r"between\s*(-?\d+\.?\d*)\s*and\s*(-?\d+\.?\d*)", question)
        if range_match:
            lower_bound = range_match.group(1)
            upper_bound = range_match.group(2)
            query = f"SELECT * FROM {selected_table} WHERE {selected_column} BETWEEN {lower_bound} AND {upper_bound};"
            return query, self.execute_sql_query(query)

    # Handle "below X"
        below_match = re.search(r"below\s*(-?\d+\.?\d*)", question)
        if below_match:
            threshold = below_match.group(1)
            query = f"SELECT * FROM {selected_table} WHERE {selected_column} < {threshold};"
            return query, self.execute_sql_query(query)

    # Handle "above X"
        above_match = re.search(r"above\s*(-?\d+\.?\d*)", question)
        if above_match:
            threshold = above_match.group(1)
            query = f"SELECT * FROM {selected_table} WHERE {selected_column} > {threshold};"
            return query, self.execute_sql_query(query)

    # Handle specific value queries: "equals to X"
        equal_match = re.search(r"equal(?:s)?\s*to\s*(-?\d+\.?\d*)", question)
        if equal_match:
            value = equal_match.group(1)
            query = f"SELECT * FROM {selected_table} WHERE {selected_column} = {value};"
            return query, self.execute_sql_query(query)

    # Default case: Select all non-null values
        query = f"SELECT * FROM {selected_table} WHERE {selected_column} IS NOT NULL;"
        return query, self.execute_sql_query(query)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec())
