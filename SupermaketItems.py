from Database import Database
from Database import ItemsTableKeys, SupermarketTableKeys, ItemTables
import json


def fetchAll():
    db = Database()
    db.startConnection()
    items = db.fetchAllItems()
    db.closeConnection()
    output = _parseItemsToDict(items)
    return output


def fetchPage(page):
    db = Database()
    db.startConnection()
    items = db.fetchPage(page)
    itemIds = []
    for item in items:
        itemIds.append(item[0])
    # countDown = db.fetchCountdownItems(itemIds)
    nwItems = db.fetchFoodStuffsItems(itemIds, "5b8f8e3b-e1a0-4a11-b16b-9cfe782c124e", ItemTables.newWorld)
    db.closeConnection()
    output = _parseSuperMarketItemsToDict(nwItems, False)
    return output


def _parseItemsToDict(items) -> list:
    output = []
    for item in items:
        outPutItem = {}
        for index, key in enumerate(ItemsTableKeys):
            if index > len(ItemsTableKeys) - 2:
                outPutItem[key.value] = item[index]
            else:
                outPutItem[key.value] = item[index].split("@")
        output.append(outPutItem)
    return output


def _parseSuperMarketItemsToDict(items, isCountdown) -> list:
    output = []
    for item in items:
        outPutItem = {}
        for index, key in enumerate(SupermarketTableKeys):
            if isCountdown and key == SupermarketTableKeys.supermarketId:
                continue
            if SupermarketTableKeys.itemId == key or SupermarketTableKeys.supermarketId == key:
                outPutItem[key.value] = item[index]
                continue

            outPutItem[key.value] = item[index].split("@")
        output.append(outPutItem)
    return output


def fetchCategories(categories: str):
    db = Database()
    db.startConnection()
    items = db.fetchItemsByCategory(categories.split(","))
    db.closeConnection()
    output = _parseItemsToDict(items)
    return output


class SupermaketItems:
    pass
