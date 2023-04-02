from dotenv import load_dotenv
import os
import MySQLdb
from pathlib import Path

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class Database:
    _connection = None
    _cursor = None

    def insertItems(self, tableName: str, values: [str]):
        sql = f"INSERT INTO {tableName} (ID, itemName, itemPrice, itemUrls, itemCategory, itemBrand) VALUES ({'%s,'*len(values[0])}"
        sql = sql[:-1] + ")"
        self._cursor.executemany(sql, values)

        self._connection.commit()

    def createTable(self, tableName: str, tableParameters: [str]):
        paramsString: str = ""
        for parameter in tableParameters:
            paramsString += (parameter + ",")
        paramsString = paramsString[:-1]
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({paramsString})")

    def dropTable(self, tableName: str):
        self._cursor.execute(f"DROP TABLE {tableName}")

    def printTables(self):
        self._cursor.execute("SHOW TABLES")
        for table in self._cursor:
            print(table)

    def fetchItems(self, tableName):
        self._cursor.execute(f"SELECT * FROM {tableName}")
        return self._cursor.fetchall()

    def testConnection(self):
        self.startConnection()
        self._cursor.execute("select @@version")
        version = self._cursor.fetchone()

        if version:
            print('Running version: ', version)
        else:
            print('Not connected.')
        self.closeConnection()

    def startConnection(self):
        self._connection = MySQLdb.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            passwd=os.getenv("PASSWORD"),
            db=os.getenv("DATABASE"),
            ssl_mode="VERIFY_IDENTITY",
            ssl={
                "ca": "/etc/ssl/cert.pem"
            }
        )
        self._cursor = self._connection.cursor()

    def closeConnection(self):
        self._connection.close()
        self._cursor = None
