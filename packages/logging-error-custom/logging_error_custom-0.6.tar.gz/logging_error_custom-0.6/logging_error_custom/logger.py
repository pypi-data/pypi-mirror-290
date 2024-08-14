import mysql.connector
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

class ExceptionLogger:
    def __init__(self, db_config=None):
        if db_config is None:
            db_config = {
                'user': os.getenv('DB_USER', 'default_user'),
                'password': os.getenv('DB_PASSWORD', 'default_password'),
                'host': os.getenv('DB_HOST', 'localhost'),
                'database': os.getenv('DB_NAME', 'default_db')
            }
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor()
            print("Database connection successful!")
            self.ensure_table_exists()
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def ensure_table_exists(self):
        """Check if the 'exceptionlog' table exists, and create it if it doesn't."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS exceptionlog (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message TEXT NOT NULL,
                    stack_trace TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Table 'exceptionlog' exists or was created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def log_exception(self, message, stack_trace):
        if self.conn is None or self.cursor is None:
            print("Database connection not established.")
            return

        try:
            # Extract the relevant part of the stack trace
            relevant_trace = self.extract_relevant_trace(stack_trace)

            query = """
            INSERT INTO exceptionlog (message, stack_trace, timestamp)
            VALUES (%s, %s, %s)
            """
            timestamp = datetime.now(timezone.utc)
            print(f"Executing query: {query}")
            print(f"With values: {message}, {relevant_trace}, {timestamp}")
            self.cursor.execute(query, (message, relevant_trace, timestamp))
            self.conn.commit()
            print("Log entry committed to database.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def extract_relevant_trace(self, stack_trace):
        # Use regex to extract the relevant part of the stack trace
        match = re.search(r'(File ".*", line \d+, in .*\n\s+.*\n\s+.*\n)', stack_trace)
        if match:
            return match.group(1)
        return stack_trace

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()