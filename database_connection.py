"""Database connection module for Tree Whisperer application."""

import logging
from typing import List, Dict, Optional

import mysql.connector
from mysql.connector import Error

from config import Config

class DatabaseConnection:
    """Handles MySQL database connections and query execution."""
    
    def __init__(self):
        self.config = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """Establish connection to the database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.logger.info("Successfully connected to MySQL database")
                return True
        except Error as e:
            self.logger.error("Error connecting to MySQL: %s", e)
            return False
        return False

    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("MySQL connection closed")

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict]:
        """Execute a SELECT query and return results as list of dictionaries"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                raise ConnectionError("Could not connect to database")

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()

            self.logger.info("Query executed successfully, returned %d rows", len(results))
            return results

        except Error as e:
            self.logger.error("Error executing query: %s", e)
            raise ConnectionError(f"Database error: {str(e)}") from e
        except (AttributeError, ValueError) as e:
            self.logger.error("Unexpected error: %s", e)
            raise RuntimeError(f"Query execution error: {str(e)}") from e

    def test_connection(self) -> bool:
        """Test the database connection"""
        try:
            if not self.connection or not self.connection.is_connected():
                return self.connect()
            return True
        except Exception as e:
            self.logger.error("Connection test failed: %s", e)
            return False

    def get_table_info(self) -> Dict:
        """Get information about available tables and their columns"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return {}

            cursor = self.connection.cursor(dictionary=True)

            # Get table names
            cursor.execute("SHOW TABLES")
            tables = [row[f'Tables_in_{Config.DB_NAME}'] for row in cursor.fetchall()]

            table_info = {}
            for table in tables:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                table_info[table] = [col['Field'] for col in columns]

            cursor.close()
            return table_info

        except (AttributeError, ValueError) as e:
            self.logger.error(f"Error getting table info: %s", e)
            return {}

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
