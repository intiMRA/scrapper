from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
from pathlib import Path

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)
class Database:
    connection = MySQLdb.connect(
      host = os.getenv("HOST"),
      user = os.getenv("USERNAME"),
      passwd = os.getenv("PASSWORD"),
      db = os.getenv("DATABASE"),
      ssl_mode = "VERIFY_IDENTITY",
      ssl = {
        "ca": "/etc/ssl/cert.pem"
      }
    )

    cursor = connection.cursor()

    def insertRow(self):
        return

    def createTable(self):
        return

    def fetchItems(self):
        return

    def testConnection(self):
        self.cursor.execute("select @@version")
        version = self.cursor.fetchone()

        if version:
            print('Running version: ', version)
        else:
            print('Not connected.')
