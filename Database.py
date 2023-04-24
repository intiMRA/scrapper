from dotenv import load_dotenv
import os
import mysql.connector
from pathlib import Path
from enum import Enum
import difflib

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class ItemTables(Enum):
    items = "items"
    countdown = "countdown"
    newWorld = "newWorld"
    pakNSave = "pakNSave"


class StoreTables(Enum):
    newWorldStores = "newWorldStores"
    pakNSaveStores = "pakNSaveStores"


class StoreTablesKeys(Enum):
    supermarketId = "id"
    name = "name"
    address = "address"
    latitude = "latitude"
    longitude = "longitude"


class StoreTablesIndexes(Enum):
    supermarketId = 0
    name = 1
    address = 2
    latitude = 3
    longitude = 4


class ItemsTableKeys(Enum):
    itemId = "itemId"
    category = "category"
    brand = "brand"


class ItemsTableKeysIndexes(Enum):
    itemId = 0
    category = 1
    brand = 2


class SupermarketTableKeys(Enum):
    itemId = "itemId"
    name = "name"
    price = "price"
    size = "size"
    photoUrl = "photoUrl"
    page = "page"
    supermarketId = "supermarketId"


class SupermarketTableIndexes(Enum):
    itemId = 0
    name = 1
    price = 2
    size = 3
    photoUrl = 4
    page = 5
    supermarketId = 6


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

    def insertStores(self, values: list, table: StoreTables):
        itemKeys = ""
        for v in StoreTablesKeys:
            itemKeys += v.value + " ,"
        itemKeys = itemKeys[:-1]
        sql = f"INSERT INTO {table.value} ({itemKeys}) VALUES ({'%s,' * len(values[0])}"
        sql = sql[:-1] + ")"
        self._cursor.executemany(sql, values)
        self._connection.commit()

    def insertItems(self, values: [str], table: ItemTables):
        itemKeys = ""
        if table == ItemTables.items:
            for v in ItemsTableKeys:
                itemKeys += v.value + " ,"
            itemKeys = itemKeys[:-1]
        else:
            itemKeys = ""
            for v in SupermarketTableKeys:
                if v == SupermarketTableKeys.supermarketId and table == ItemTables.countdown:
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

        # supermarketStores
        # id, name, address, latitude, longitude

        itemKeys = ""
        for v in ItemsTableKeys:
            itemKeys += v.value + " MEDIUMTEXT,"
        itemKeys = itemKeys[:-1]
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {ItemTables.items.value} ({itemKeys})")
        for table in ItemTables:
            if table == ItemTables.items:
                continue
            itemKeys = ""
            for v in SupermarketTableKeys:
                if v == SupermarketTableKeys.supermarketId and table == ItemTables.countdown:
                    continue
                itemKeys += v.value + " LONGTEXT,"
            itemKeys = itemKeys[:-1]
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table.value} ({itemKeys})")

        for storeTable in StoreTables:
            storeKeys = ""
            for key in StoreTablesKeys:
                storeKeys += key.value + " MEDIUMTEXT,"
            storeKeys = storeKeys[:-1]
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {storeTable.value} ({storeKeys})")

    def dropTables(self):
        for table in ItemTables:
            self._cursor.execute(f"DROP TABLE {table.value}")

        for table in StoreTables:
            self._cursor.execute(f"DROP TABLE {table.value}")

    def printTables(self):
        self._cursor.execute("SHOW TABLES")
        for table in self._cursor:
            print(table)

    def fetchAllItems(self, table: Enum):
        self._cursor.execute(f"SELECT * FROM {table.value}")
        return self._cursor.fetchall()

    def fetchPage(self, page):
        self._cursor.execute(f"SELECT * FROM {ItemTables.items.value} "
                             f"WHERE {ItemsTableKeys.page.value} = {page}")
        return self._cursor.fetchall()

    def fetchItemsById(self, itemIds):
        query = ''
        for itemId in itemIds:
            query += f'"{itemId}",'
        query = query[:-1]
        sql = f"SELECT * FROM {ItemTables.items.value} " \
              f"WHERE {ItemsTableKeys.itemId.value} IN ({query})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByName(self, query, newWorldIds: [str], packNSaveIds: [str]):
        nwStoreIdsQuery = ''
        for storeId in newWorldIds:
            nwStoreIdsQuery += f'"{storeId}",'
        nwStoreIdsQuery = nwStoreIdsQuery[:-1]

        psStoreIdsQuery = ''
        for storeId in packNSaveIds:
            psStoreIdsQuery += f'"{storeId}",'
        psStoreIdsQuery = psStoreIdsQuery[:-1]

        self._cursor.execute(f"SELECT * FROM {ItemTables.countdown.value} "
                             f"WHERE {SupermarketTableKeys.name.value} "
                             f"like '%{query}%' "
                             f"LIMIT 1000")

        countdownItems = self._cursor.fetchall()

        self._cursor.execute(f"SELECT * FROM {ItemTables.newWorld.value} "
                             f"WHERE ({SupermarketTableKeys.name.value} "
                             f"like '%{query}%' "
                             f"AND {SupermarketTableKeys.supermarketId.value} IN ({nwStoreIdsQuery}))"
                             f"LIMIT 1000")

        newWorldItems = self._cursor.fetchall()

        self._cursor.execute(f"SELECT * FROM {ItemTables.pakNSave.value} "
                             f"WHERE ({SupermarketTableKeys.name.value} "
                             f"like '%{query}%' "
                             f"AND {SupermarketTableKeys.supermarketId.value} IN ({psStoreIdsQuery}))"
                             f"LIMIT 1000")

        packNSaveItems = self._cursor.fetchall()

        return {
            ItemTables.countdown.value: countdownItems,
            ItemTables.newWorld.value: newWorldItems,
            ItemTables.pakNSave.value: packNSaveItems,
        }

    def fetchCountdownItemsByIds(self, itemIds):
        query = ''
        for itemId in itemIds:
            query += f'"{itemId}",'
        query = query[:-1]
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.itemId.value} IN" \
              f" ({query})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchCountdownItemsByPage(self, page: str):
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.page.value} = {page}"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsIds(self, itemIds, storeIds, table: ItemTables):
        itemIdsQuery = ''
        for itemId in itemIds:
            itemIdsQuery += f'"{itemId}",'
        itemIdsQuery = itemIdsQuery[:-1]

        storeIdsQuery = ''
        for storeId in storeIds:
            storeIdsQuery += f'"{storeId}",'
        storeIdsQuery = storeIdsQuery[:-1]

        sql = f"SELECT * FROM {table.value} " \
              f"WHERE {SupermarketTableKeys.itemId.value} IN ({itemIdsQuery}) " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsQuery})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsByPage(self, page: str, storeIds, table: ItemTables):
        storeIdsQuery = ''
        for storeId in storeIds:
            storeIdsQuery += f'"{storeId}",'
        storeIdsQuery = storeIdsQuery[:-1]

        sql = f"SELECT * FROM {table.value} " \
              f"WHERE ({SupermarketTableKeys.page.value} = {page} " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsQuery}))"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByCategory(self, categories):
        query = ''
        for category in categories:
            query += f"{ConcatcKeys.category.value} like '%{category}%' OR "
        query = query[:-4]
        fullQuery = f"SELECT * FROM {ItemTables.items.value} " \
                    f"WHERE {query}"
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
        self._connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            passwd=os.getenv("PASSWORD"),
            db=os.getenv("DATABASE"),
            use_pure=True
        )
        self._cursor = self._connection.cursor()

    def closeConnection(self):
        self._connection.close()
        self._cursor = None