import pyodbc
from typing import Optional, Dict, Text
from .database_connector import DatabaseConnector
from sqlalchemy import create_engine, inspect, text


class MSSQLConnector(DatabaseConnector):
    name = 'MSSQL'

    def __init__(self, name: Text, connection_data: Optional[Dict]):
        super().__init__(name, connection_data)

    def create_connection(self):
        connection_string = f"mssql+pyodbc://{self.connection_data['user']}:{self.connection_data['password']}@{self.connection_data['host']}:{self.connection_data['port']}/{self.connection_data['database']}"
        try:
            driver = pyodbc.drivers()[-1]
        except IndexError:
            raise Exception("No MSSQL driver found. Please install a driver for MSSQL.")

        return create_engine(f"{connection_string}?driver={driver}")