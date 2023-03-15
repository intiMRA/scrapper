from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
from pathlib import Path

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)
class Database:
    _connection = None
    _cursor = None

    def insertRow(self):
        return

    def createTable(self, tableName: str, tablePatameters: [str]):
        paramsString: str = ""
        for parameter in tablePatameters:
            paramsString += (parameter + ",")
        paramsString = paramsString[:-1]
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({paramsString})")

    def printTables(self):
        self.cursor.execute("SHOW TABLES")
        for table in self.cursor:
            print(table)
    def fetchItems(self):
        return

    def testConnection(self):
        self.cursor.execute("select @@version")
        version = self.cursor.fetchone()

        if version:
            print('Running version: ', version)
        else:
            print('Not connected.')

    def startConnection(self):
        self.connection = MySQLdb.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USERNAME"),
            passwd = os.getenv("PASSWORD"),
            db = os.getenv("DATABASE"),
            ssl_mode = "VERIFY_IDENTITY",
            ssl = {
                "ca": "/etc/ssl/cert.pem"
            }
        )
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        self.connection.close()
        self.cursor = None


