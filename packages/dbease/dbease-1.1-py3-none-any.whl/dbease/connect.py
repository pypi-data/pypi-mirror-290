import sqlite3
import configparser
import os

# Define the path to the configuration file
config_path = os.path.join(os.getcwd(), 'database.ini')

# Create a default configuration file if it does not exist
if not os.path.exists(config_path):
    with open(config_path, 'w') as config_file:
        config_file.write("[user]\n")
        config_file.write("first_name = Mohammad\n")
        config_file.write("last_name = Mohammadi\n")
        config_file.write("username = Aytola\n")
        config_file.write("password = TestPassword\n")
        config_file.write("age = 21\n")
        config_file.write("register = 08/12/2024,12:16:11\n")
        config_file.write("\n")
        config_file.write("[admin]\n")
        config_file.write("first_name = Mohammad\n")
        config_file.write("last_name = Mohammadi\n")
        config_file.write("username = Aytola\n")
        config_file.write("password = TestPassword\n")

# Initialize the configuration parser
config = configparser.ConfigParser()
config.read(config_path)

class Database:
    """
    The `Database` class handles the connection to an SQLite database and the creation of tables
    based on the provided `database.ini` configuration file.

    Attributes:
    db_path (str): The path to the SQLite database file.
    """
    def __init__(self, db_path: str):
        """
        Initializes the `Database` class with the path to the SQLite database file.

        Args:
        db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path

    def __infer_type(self,value):
        """
        Infers the type of a value for database column definitions.

        Args:
        value (str): The value to infer the type from.

        Returns:
        type or str: The inferred type of the value, or "datetime" if it matches that type.
        """
        try:
            if '.' in value:
                return float(value)
            elif "datetime" == value:
                return "datetime"
            else:
                return int(value)
        except ValueError:
            return value

    def connect(self):
        """
        Connects to the SQLite database and creates tables if they do not exist.

        Returns:
        sqlite3.Connection: The SQLite connection object.
        """
        conn = sqlite3.connect(self.db_path)
        self.tables_exist(conn)
        return conn

    def tables_exist(self, conn):
        """
        Checks if the tables defined in the configuration file already exist in the database.
        Creates any tables that do not exist.

        Args:
        conn (sqlite3.Connection): The SQLite connection object.
        """
        cursor = conn.cursor()
        existing_tables = []
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor.fetchall():
            existing_tables.append(row[0])
        for table in config.sections():
            if table not in existing_tables:
                self.create_tables(conn,table)

    def create_tables(self, conn,table):
        """
        Creates a table in the SQLite database based on the configuration file.

        Args:
        conn (sqlite3.Connection): The SQLite connection object.
        table (str): The name of the table to create.
        """
        cursor = conn.cursor()
        sql = f"CREATE TABLE IF NOT EXISTS {table} (\n"
        column_defs = []
        
        for key, value in config.items(table):
            if key == "id":
                column_defs.append("id INTEGER PRIMARY KEY")
                continue
            typeValue = type(self.__infer_type(value))
            if typeValue == "datetime":
                column_defs.append(f"    {key} DATETIME NOT NULL")
            elif typeValue == str:
                column_defs.append(f"    {key} TEXT NOT NULL")
            elif typeValue == int:
                column_defs.append(f"    {key} INTEGER NOT NULL") 
            elif typeValue == float:
                column_defs.append(f"    {key} REAL NOT NULL") 
        sql += ",\n".join(column_defs)
        sql += "\n);"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
