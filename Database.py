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
    _debug = False

    def __init__(self, debug=False):
        self._debug = debug

    def insertStores(self, values: list, table: StoreTables):
        if self._debug:
            return
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

        valuesString = ','.join(['%s'] * len(values[0]))
        if self._debug:
            with open(f'{table.value}.txt', mode="a+") as file:
                for value in values:
                    file.write(','.join(value) + "\n")
            return

        sql = f"INSERT INTO {table.value} ({itemKeys}) VALUES ({valuesString})"
        self._cursor.executemany(sql, values)
        self._connection.commit()

    def createTable(self):
        if self._debug:
            for table in ItemTables:
                f = open(f"{table.value}.txt", mode="w")
                f.close()
            return
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
        if self._debug:
            for table in ItemTables:
                f = open(f"{table.value}.txt", mode="w")
                f.close()
            return
        for table in ItemTables:
            self._cursor.execute(f"DROP TABLE {table.value}")

        for table in StoreTables:
            self._cursor.execute(f"DROP TABLE {table.value}")

    def printTables(self):
        if self._debug:
            return
        self._cursor.execute("SHOW TABLES")
        for table in self._cursor:
            print(table)

    def fetchAllItems(self, table: Enum):
        if self._debug:
            return
        self._cursor.execute(f"SELECT * FROM {table.value}")
        return self._cursor.fetchall()

    def fetchItemsById(self, itemIds):
        if self._debug:
            itemIds = set(itemIds)
            with open(f'{ItemTables.items.value}.txt', mode='r') as file:
                items = file.readlines()
                returnItems = []
                for item in items:
                    splitItem = item.replace("\n", "").split(',')
                    if splitItem[ItemsTableKeysIndexes.itemId.value] in itemIds:
                        returnItems.append(splitItem)
                return returnItems
        itemIdsString = ', '.join(f'"{w}"' for w in itemIds)
        sql = f"SELECT * FROM {ItemTables.items.value} " \
              f"WHERE {ItemsTableKeys.itemId.value} IN ({itemIdsString})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByName(self, query, newWorldIds: [str], packNSaveIds: [str]):
        countdownItems = []
        newWorldItems = []
        packNSaveItems = []
        if self._debug:
            with open(f'{ItemTables.countdown.value}.txt', mode='r') as countdownFile:
                items = countdownFile.readlines()
                for item in items:
                    splitItem = item.split(",")
                    if query in splitItem[SupermarketTableIndexes.name.value]:
                        countdownItems.append(splitItem)
                    if len(countdownItems) > 1000:
                        break

            with open(f'{ItemTables.newWorld.value}.txt', mode='r') as newWorldFile:
                items = newWorldFile.readlines()
                for item in items:
                    splitItem = item.split(",")
                    if query in splitItem[SupermarketTableIndexes.name.value] \
                            and splitItem[SupermarketTableIndexes.supermarketId.value] in newWorldIds:
                        newWorldItems.append(splitItem)
                    if len(newWorldItems) > 1000:
                        break

            with open(f'{ItemTables.pakNSave.value}.txt', mode='r') as packNSaveFile:
                items = packNSaveFile.readlines()
                for item in items:
                    splitItem = item.split(",")
                    if query in splitItem[SupermarketTableIndexes.name.value] \
                            and splitItem[SupermarketTableIndexes.supermarketId.value] in packNSaveIds:
                        packNSaveItems.append(splitItem)
                    if len(packNSaveItems) > 1000:
                        break
        else:
            self._cursor.execute(f"SELECT * FROM {ItemTables.countdown.value} "
                                 f"WHERE {SupermarketTableKeys.name.value} "
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
        if self._debug:
            with open(f'{ItemTables.countdown.value}.txt', mode='r') as countdownFile:
                items = countdownFile.readlines()
                returnItems = []
                for item in items:
                    splitItem = item.replace("\n", "").split(',')
                    if splitItem[SupermarketTableIndexes.itemId.value] in itemIds:
                        returnItems.append(splitItem)
                return returnItems
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.itemId.value} IN" \
              f" ({','.join(itemIds)})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchCountdownItemsByPage(self, page: str):
        if self._debug:
            with open(f'{ItemTables.countdown.value}.txt', mode='r') as countdownFile:
                items = countdownFile.readlines()
                returnItems = []
                for item in items:
                    splitItem = item.replace("\n", "").split(',')
                    if splitItem[SupermarketTableIndexes.page.value] == page:
                        returnItems.append(splitItem)
                return returnItems
        sql = f"SELECT * FROM {ItemTables.countdown.value} WHERE" \
              f" {SupermarketTableKeys.page.value} = {page}"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsIds(self, itemIds, storeIds, table: ItemTables):
        if self._debug:
            with open(f'{table.value}.txt', mode='r') as file:
                items = file.readlines()
                returnItems = []
                for item in items:
                    splitItem = item.replace("\n", "").split(',')
                    if splitItem[SupermarketTableIndexes.itemId.value] in itemIds \
                            and splitItem[SupermarketTableIndexes.supermarketId.value] in storeIds:
                        returnItems.append(splitItem)
                return returnItems
        itemIdsString = ', '.join(f'"{w}"' for w in itemIds)
        storeIdsString = ', '.join(f'"{w}"' for w in storeIds)
        sql = f"SELECT * FROM {table.value} " \
              f"WHERE {SupermarketTableKeys.itemId.value} IN ({itemIdsString}) " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsString})"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchFoodStuffsItemsByPage(self, page: str, storeIds, table: ItemTables):
        if self._debug:
            with open(f'{table.value}.txt', mode='r') as file:
                items = file.readlines()
                returnItems = []
                for item in items:
                    splitItem = item.replace("\n", "").split(',')
                    if splitItem[SupermarketTableIndexes.page.value] == page \
                            and splitItem[SupermarketTableIndexes.supermarketId.value] in storeIds:
                        returnItems.append(splitItem)
                return returnItems
        storeIdsString = ', '.join(f'"{w}"' for w in storeIds)
        sql = f"SELECT * FROM {table.value} " \
              f"WHERE ({SupermarketTableKeys.page.value} = {page} " \
              f"AND {SupermarketTableKeys.supermarketId.value} IN ({storeIdsString}))"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetchItemsByCategory(self, categories):
        if self._debug:
            return
        query = ' OR '.join([f"{ConcatcKeys.category.value} like '%{category}%'" for category in categories])
        fullQuery = f"SELECT * FROM {ItemTables.items.value} " \
                    f"WHERE {query}"
        self._cursor.execute(fullQuery)
        return self._cursor.fetchall()

    def testConnection(self):
        if self._debug:
            return
        self.startConnection()
        self._cursor.execute("select @@version")
        version = self._cursor.fetchone()

        if version:
            print('Running version: ', version)
        else:
            print('Not connected.')
        self.closeConnection()

    def startConnection(self):
        if self._debug:
            return
        self._connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            passwd=os.getenv("PASSWORD"),
            db=os.getenv("DATABASE"),
            use_pure=True
        )
        self._cursor = self._connection.cursor()

    def closeConnection(self):
        if self._debug:
            return
        self._connection.close()
        self._cursor = None
