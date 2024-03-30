import pyodbc
import yaml

with open('configuration_data.yaml') as f:
    config = yaml.safe_load(f)

server = config["DBServer"]
database = config["DBDatabaseName"]
username = config["DBUsername"]
password = config["DBPassword"]

connection_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

connection = pyodbc.connect(connection_str)


class DBConnection:
    @staticmethod
    def database_cursor():
        return connection.cursor()

    @staticmethod
    def close_connection():
        connection.close()
