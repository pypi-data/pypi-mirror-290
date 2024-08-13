from . import connecter
from dataclasses import make_dataclass
import os

myclient = connecter.Database(os.path.join(os.getcwd(), 'DataBase.db')).connect()

class DataBase:
    """
    The `DataBase` class provides a simple interface for working with an SQLite database,
    allowing users to interact with the database without needing to know SQL.

    This class allows users to automatically create tables based on a `database.ini` file,
    insert data, and perform CRUD operations.

    Attributes:
    table (str): The name of the current table for CRUD operations.
    data (dict): The data to be inserted or updated in the database.
    query (dict): The search criteria for updating or querying data.
    conn: The database connection object.
    cursor: The database cursor object.
    """
    def __init__(self, table: str = None, query: dict = None, data: dict = None):
        """
        Initializes the `DataBase` class, sets up the database connection, and loads tables
        from the `database.ini` file.

        Args:
        table (str): The name of the table to work with.
        query (dict): The criteria for querying or updating records.
        data (dict): The data to be inserted or updated.
        """
        self.table = table
        self.data = data
        self.query = query
        self.conn = myclient
        self.cursor = self.conn.cursor()

    def __infer_type(self,value):
        """
        Infers the type of a value for database operations.

        Args:
        value (str): The value to infer type from.

        Returns:
        int, float, str, or "datetime": The inferred type of the value.
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

    @property
    def nametable(self):
        """
        Retrieves the names and columns of the tables defined in the `database.ini` file.

        Returns:
        DataClass: A dataclass instance representing table names and columns.
        """
        data_dict = dict()
        for table in connecter.config.sections():
            data_dict[table] = table
        fields = [(key, type(self.__infer_type(value))) for key, value in data_dict.items()]
        data = [self.__infer_type(value) for value in data_dict.values()]
        DataClass = make_dataclass("nameLoadTable", fields)
        return DataClass(*data)
    
    def __dataclass(self,table,data):
        """
        Creates a dataclass for the given table with the provided data.

        Args:
        table (str): The name of the table.
        data (tuple): The data to populate the dataclass with.

        Returns:
        DataClass: A dataclass instance representing the table's structure.
        """
        data_dict = {key: value for key, value in connecter.config[table].items()}
        fields = [(key, type(self.__infer_type(value))) for key, value in data_dict.items()]
        DataClass = make_dataclass(table, fields)
        return DataClass(*data)
        
    @property
    def insert(self):
        """
        Inserts data into the current table.

        Returns:
        int: The ID of the last inserted row.

        Raises:
        ValueError: If `data` is not set.
        """
        if self.data is None:
            raise ValueError("Data is not set.")
        columns = ', '.join(self.data.keys())
        placeholders = ', '.join(['?'] * len(self.data))
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(self.data.values()))
        self.conn.commit()
        return self.cursor.lastrowid

    @property
    def get(self):
        """
        Retrieves data from the current table based on the query criteria.

        Returns:
        list: A list of dataclass instances representing the queried records.
        """
        listdata = []
        query = ' AND '.join([f"{k} = ?" for k in self.query.keys()])
        sql = f"SELECT * FROM {self.table} WHERE {query}"
        self.cursor.execute(sql, tuple(self.query.values()))
        for item in self.cursor.fetchall():
            listdata.append(self.__dataclass(self.table,item))
        return listdata

    @property
    def check(self):
        """
        Checks if there are any records that match the query criteria.

        Returns:
        bool: True if matching records are found, False otherwise.
        """
        result = self.get
        return bool(result)
    
    @property
    def all(self):
        """
        Retrieves all data from the current table.

        Returns:
        list: A list of dataclass instances representing all records in the table.
        """
        listdata = []
        sql = f"SELECT * FROM {self.table}"
        self.cursor.execute(sql)
        for item in self.cursor.fetchall():
            listdata.append(self.__dataclass(self.table,item))
        return listdata

    @property
    def set(self):
        """
        Updates data in the current table based on the query criteria.

        Raises:
        ValueError: If `data` or `query` is not set.
        """
        set_query = ', '.join([f"{k} = ?" for k in self.data.keys()])
        query = ' AND '.join([f"{k} = ?" for k in self.query.keys()])
        sql = f"UPDATE {self.table} SET {set_query} WHERE {query}"
        self.cursor.execute(sql, tuple(self.data.values()) + tuple(self.query.values()))
        self.conn.commit()

    @property
    def delete(self):
        """
        Deletes records from the current table based on the query criteria.

        Raises:
        ValueError: If `query` is not set.
        """
        query = ' AND '.join([f"{k} = ?" for k in self.query.keys()])
        sql = f"DELETE FROM {self.table} WHERE {query}"
        self.cursor.execute(sql, tuple(self.query.values()))
        self.conn.commit()


