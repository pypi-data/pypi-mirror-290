import mysql.connector
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ExceptionLogger:
    def __init__(self, db_config=None):
        if db_config is None:
            db_config = {
                "user": os.getenv("DB_USER", "default_user"),
                "password": os.getenv("DB_PASSWORD", "default_password"),
                "host": os.getenv("DB_HOST", "localhost"),
                "database": os.getenv("DB_NAME", "ApplicationPerfDB"),
            }
        self.db_config = db_config
        self.conn = None
        self.cursor = None
        try:
            self.connect_to_database()
            self.ensure_database_and_tables_exist()
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def connect_to_database(self):
        """Connect to the MySQL server and select the specified database."""
        try:
            self.conn = mysql.connector.connect(
                user=self.db_config["user"], password=self.db_config["password"],
                host=self.db_config["host"]
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            self.cursor.execute(f"USE {self.db_config['database']}")
            print(f"Connected to database: {self.db_config['database']}")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            raise

    def ensure_database_and_tables_exist(self):
        """Ensure that the required database and tables exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ExceptionCategory (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category VARCHAR(50) NOT NULL,
                    description VARCHAR(100)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ApplicationTypeMaster (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type VARCHAR(50) NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ApplicationMaster (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    type_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (type_id) REFERENCES ApplicationTypeMaster(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ApplicationException (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    application_id INT,
                    category_id INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT,
                    stack_trace TEXT,
                    FOREIGN KEY (application_id) REFERENCES ApplicationMaster(id),
                    FOREIGN KEY (category_id) REFERENCES ExceptionCategory(id)
                )
            """)
            print("Tables ensured successfully.")
        except mysql.connector.Error as err:
            print(f"Error ensuring tables: {err}")
            raise

    def ensure_application_exists(self, application_name, application_type):
        """Check if the application exists in the ApplicationMaster table and add it if necessary."""
        try:
            self.cursor.execute("SELECT id FROM ApplicationTypeMaster WHERE type = %s", (application_type,))
            type_id = self.cursor.fetchone()
            if type_id is None:
                self.cursor.execute("INSERT INTO ApplicationTypeMaster (type) VALUES (%s)", (application_type,))
                self.conn.commit()
                type_id = self.cursor.lastrowid
            else:
                type_id = type_id[0]
            self.cursor.execute("SELECT id FROM ApplicationMaster WHERE name = %s", (application_name,))
            application_id = self.cursor.fetchone()
            if application_id is None:
                self.cursor.execute("INSERT INTO ApplicationMaster (name, type_id) VALUES (%s, %s)", (application_name, type_id))
                self.conn.commit()
                application_id = self.cursor.lastrowid
            else:
                application_id = application_id[0]
            return application_id
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            raise

    def log_exception(self, application_name, application_type, category, message, stack_trace):
        if self.conn is None or self.cursor is None:
            print("Database connection not established.")
            return
        try:
            application_id = self.ensure_application_exists(application_name, application_type)
            self.cursor.execute("SELECT id FROM ExceptionCategory WHERE category = %s", (category,))
            category_id = self.cursor.fetchone()
            if category_id is None:
                self.cursor.execute("INSERT INTO ExceptionCategory (category) VALUES (%s)", (category,))
                self.conn.commit()
                category_id = self.cursor.lastrowid
            else:
                category_id = category_id[0]
            query = """
                INSERT INTO ApplicationException (application_id, category_id, error_message, stack_trace, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """
            timestamp = datetime.now(timezone.utc)
            self.cursor.execute(query, (application_id, category_id, message, stack_trace, timestamp))
            self.conn.commit()
            print("Log entry committed to database.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
