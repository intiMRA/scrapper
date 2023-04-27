from dotenv import load_dotenv
import os
import mysql.connector
from pathlib import Path
from enum import Enum

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class ItemTables(Enum):
    items: str = "items"
    countdown: str = "countdown"
    newWorld: str = "newWorld"
    pakNSave: str = "pakNSave"


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
        sql = f"INSERT INTO {table.value} ({','.join([key.value for key in StoreTablesKeys])}) " \
              f"VALUES ({','.join(['%s'] * len(values[0]))})"
        self._cursor.executemany(sql, values)
        self._connection.commit()

    def insertItems(self, values: [str], table: ItemTables):
        itemKeys = ",".join([key.value for key in SupermarketTableKeys
                             if table != ItemTables.countdown or
                             (key != SupermarketTableKeys.supermarketId and table == ItemTables.countdown)])

        if table == ItemTables.items:
            itemKeys = ",".join([key.value for key in ItemsTableKeys])

        sql = f"INSERT INTO {table.value} ({itemKeys}) VALUES ({','.join(['%s'] * len(values[0]))})"
        print(sql)
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
        item_keys = ",".join([v.value + " MEDIUMTEXT" for v in ItemsTableKeys])
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {ItemTables.items.value} ({item_keys})")

        for table in ItemTables:
            if table == ItemTables.items:
                continue
            table_keys = ",".join([v.value + " LONGTEXT" for v in SupermarketTableKeys if
                                   not (v == SupermarketTableKeys.supermarketId and table == ItemTables.countdown)])
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table.value} ({table_keys})")

        store_keys = ",".join([key.value + " MEDIUMTEXT" for key in StoreTablesKeys])
        for store_table in StoreTables:
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {store_table.value} ({store_keys})")

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

    def fetchItemsById(self, itemIds):
        itemIdsString = ', '.join(f'"{w}"' for w in itemIds)
        sql = f"SELECT * FROM {ItemTables.items.value} " \
              f"WHERE {ItemsTableKeys.itemId.value} IN ({itemIdsString})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByName(self, query, newWorldIds: [str], packNSaveIds: [str]):
        self._cursor.execute(f"SELECT * FROM {ItemTables.countdown.value} "
                             f"WHERE ({SupermarketTableKeys.name.value} "
                             f"like '%{query}%' LIMIT 1000")

        countdownItems = self._cursor.fetchall()

        self._cursor.execute(f"SELECT * FROM {ItemTables.newWorld.value} "
                             f"WHERE ({SupermarketTableKeys.name.value} "
                             f"like %s "
                             f"AND {SupermarketTableKeys.supermarketId.value} "
                             f"IN ({','.join(['%s'] * len(newWorldIds))}))"
                             f"LIMIT 1000", ('%' + query + '%',) + tuple(newWorldIds))

        newWorldItems = self._cursor.fetchall()

        self._cursor.execute(f"SELECT * FROM {ItemTables.pakNSave.value} "
                             f"WHERE ({SupermarketTableKeys.name.value} "
                             f"like %s "
                             f"AND {SupermarketTableKeys.supermarketId.value} "
                             f"IN ({','.join(['%s'] * len(packNSaveIds))}))"
                             f"LIMIT 1000", ('%' + query + '%',) + tuple(packNSaveIds))

        packNSaveItems = self._cursor.fetchall()

        return {
            ItemTables.countdown.value: countdownItems,
            ItemTables.newWorld.value: newWorldItems,
            ItemTables.pakNSave.value: packNSaveItems,
        }

    def fetchCountdownItemsByIds(self, itemIds):
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.itemId.value} IN" \
              f" ({','.join(itemIds)})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchCountdownItemsByPage(self, page: str):
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.page.value} = {page}"
        print(sql)
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsIds(self, itemIds, storeIds, table: ItemTables):
        itemIdsString = ', '.join(f'"{w}"' for w in itemIds)
        storeIdsString = ', '.join(f'"{w}"' for w in storeIds)
        sql = f"SELECT * FROM {table.value} " \
              f"WHERE {SupermarketTableKeys.itemId.value} IN ({itemIdsString}) " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsString})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsByPage(self, page: str, storeIds, table: ItemTables):
        storeIdsString = ', '.join(f'"{w}"' for w in storeIds)
        sql = f"SELECT * FROM {table.value} " \
              f"WHERE ({SupermarketTableKeys.page.value} = {page} " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsString}))"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByCategory(self, categories):
        query = ' OR '.join([f"{ConcatcKeys.category.value} like '%{category}%'" for category in categories])
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
