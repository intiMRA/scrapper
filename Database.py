from dotenv import load_dotenv
import os
import MySQLdb
from pathlib import Path
from enum import Enum
dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)

class ConcatcKeys(Enum):
    newWorldItemNames = "newWorldItemNames"
    newWorldPrices = "newWorldPrices"
    newWorldphotoUrls = "newWorldphotoUrls"
    newWorldSizes = "newWorldSizes"

    packNSaveItemNames = "packNSaveItemNames"
    packNSavePrices = "packNSavePrices"
    packNSavephotoUrls = "packNSavephotoUrls"
    packNSaveSizes = "packNSaveSizes"

    countdownItemNames = "countdownItemNames"
    countdownPrices = "countdownPrices"
    countdownphotoUrls = "countdownphotoUrls"
    countdownSizes = "countdownSizes"

    category = "category"
    brand = "brand"

class Database:
    _connection = None
    _cursor = None
    _tableName = "items"

    def insertItems(self, values: [str]):
        parameterKeys = ""
        for v in ConcatcKeys:
            parameterKeys += v.value + ","
        parameterKeys = 'page'
        sql = f"INSERT INTO {self._tableName} ({parameterKeys}) VALUES ({'%s,'*len(values[0])}"
        sql = sql[:-1] + ")"
        self._cursor.executemany(sql, values)

        self._connection.commit()

    def createTable(self):
        parameterKeys = ""
        for v in ConcatcKeys:
            parameterKeys += v.value + " MEDIUMTEXT,"
        parameterKeys += "page VARCHAR(255)"
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._tableName} ({parameterKeys})")

    def dropTable(self):
        self._cursor.execute(f"DROP TABLE {self._tableName}")

    def printTables(self):
        self._cursor.execute("SHOW TABLES")
        for table in self._cursor:
            print(table)

    def fetchAllItems(self):
        self._cursor.execute(f"SELECT * FROM {self._tableName}")
        return self._cursor.fetchall()

    def fetchItemsByCategory(self, category):
        self._cursor.execute(f"SELECT * FROM {self._tableName} WHERE {ConcatcKeys.category.value} like '%{category}%'")
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
