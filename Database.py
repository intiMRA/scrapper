from dotenv import load_dotenv
import os
import MySQLdb
from pathlib import Path
from enum import Enum

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class Tables(Enum):
    items = "items"
    countdown = "countdown"
    newWorld = "newWorld"
    pakNSave = "pakNSave"


class ItemsTableKeys(Enum):
    itemId = "itemId"
    category = "category"
    brand = "brand"
    page = "page"


class SupermarketTableKeys(Enum):
    itemId = "itemId"
    name = "name"
    price = "price"
    size = "size"
    photoUrl = "photoUrl"
    supermarketId = "supermarketId"


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

    def insertItems(self, values: [str], table: Tables):
        itemKeys = ""
        if table == Tables.items:
            for v in ItemsTableKeys:
                itemKeys += v.value + " ,"
            itemKeys = itemKeys[:-1]
        else:
            itemKeys = ""
            for v in SupermarketTableKeys:
                if v == SupermarketTableKeys.supermarketId and table == Tables.countdown:
                    continue
                itemKeys += v.value + " ,"
            itemKeys = itemKeys[:-2]

        sql = f"INSERT INTO {table.value} ({itemKeys}) VALUES ({'%s,' * len(values[0])}"
        sql = sql[:-1] + ")"
        self._cursor.executemany(sql, values)
        self._connection.commit()

    def createTable(self):
        # items
        # itemId, category, brand, page

        # countdown
        # itemId, name, size, price, url

        # foodStuffs
        # itemId, supermarketId, name, size, price, url

        itemKeys = ""
        for v in ItemsTableKeys:
            itemKeys += v.value + " MEDIUMTEXT,"
        itemKeys = itemKeys[:-1]
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {Tables.items.value} ({itemKeys})")
        for table in Tables:
            if table == Tables.items:
                continue
            itemKeys = ""
            for v in SupermarketTableKeys:
                if v == SupermarketTableKeys.supermarketId and table == Tables.countdown:
                    continue
                itemKeys += v.value + " LONGTEXT,"
            itemKeys = itemKeys[:-1]
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table.value} ({itemKeys})")

    def dropTables(self):
        for table in Tables:
            self._cursor.execute(f"DROP TABLE {table.name}")

    def printTables(self):
        self._cursor.execute("SHOW TABLES")
        for table in self._cursor:
            print(table)

    def fetchAllItems(self, table: Tables):
        self._cursor.execute(f"SELECT * FROM {table.value}")
        return self._cursor.fetchall()

    def fetchPage(self, page):
        self._cursor.execute(f"SELECT * FROM {Tables.items.value} WHERE {ItemsTableKeys.page.value} = {page}")
        return self._cursor.fetchall()

    def fetchCountdownItems(self, itemIds):
        query = ''
        for itemId in itemIds:
            query += f'"{itemId}",'
        query = query[:-1]
        sql = f"SELECT * FROM {Tables.countdown.value} WHERE {SupermarketTableKeys.itemId.value} IN ({query})"
        print(sql)
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItems(self, itemIds, supermarketId, table: Tables):
        query = ''
        for itemId in itemIds:
            query += f'"{itemId}",'
        query = query[:-1]
        sql = f"SELECT * FROM {table.value} WHERE {SupermarketTableKeys.itemId.value} IN ({query}) " \
              f"AND {SupermarketTableKeys.supermarketId.value} like '%{supermarketId}%'"
        print(sql)
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    def fetchItemsByCategory(self, categories):
        query = ''
        for category in categories:
            query += f"{ConcatcKeys.category.value} like '%{category}%' OR "
        query = query[:-4]
        fullQuery = f"SELECT * FROM {Tables.items.value} WHERE {query}"
        print(fullQuery)
        self._cursor.execute(fullQuery)
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
