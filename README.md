# Define the content for the README file
readme_content = """
# Database Query Chat Application

This is a PyQt6-based GUI application that allows users to interact with a PostgreSQL database using natural language queries. The application parses user input, generates appropriate SQL queries, and displays the results in a tabular format.

## Features

- **Natural Language Processing**: Users can ask questions like:
  - "Show rows where value is between 50 and 150."
  - "Show rows where value is above 100."
  - "Show rows where value equals 75."
- **Dynamic SQL Query Generation**: Automatically generates SQL queries based on user input.
- **Interactive Chat Interface**: Displays user queries and system responses in a chat-like interface.
- **Results Display**: Shows query results in a table with options to resize and stretch columns.
- **Download Results**: Allows users to download the results as a CSV file.

---

## Prerequisites

1. **Python 3.8+**
2. **PostgreSQL Database**
3. Required Python libraries:
   - `PyQt6`
   - `SQLAlchemy`
   - `psycopg2`
   - `csv`
   - `re`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>

Install Dependencies: Use pip to install the required libraries:pip install PyQt6 sqlalchemy psycopg2
Set Up PostgreSQL Database:

Ensure you have a PostgreSQL database running.
Update the database connection string in the code:   engine = create_engine("postgresql+psycopg2://<username>:<password>@<host>/<database_name>")

Usage
Run the Application:python app.py
Interact with the GUI:

Type your query in the input box (e.g., "Show rows where value is between 50 and 150").
View the generated SQL query and the results in the chat interface.
Download results by clicking the "Download Results" button.
Supported Queries:

Range Queries: "between X and Y", "below X", "above X"
Specific Values: "equals to X"
Default: Selects all non-null values.




