import difflib
from Database import Database
from Database import ItemsTableKeys, SupermarketTableKeys, SupermarketTableIndexes, ItemTables, \
    StoreTables, StoreTablesKeys, StoreTablesIndexes, ItemsTableKeysIndexes
from geopy import distance
from typing import NewType

ResponseType = NewType("Response", dict[str, list[list[dict, any]]])


def fetchStores(lat: str, long: str, radius: str) -> dict[str, list[dict[str, str]]]:
    radius = float(radius)
    location = (float(lat), float(long))
    db = Database()
    db.startConnection()
    newWorldStores = db.fetchAllItems(StoreTables.newWorldStores)
    packNSaveStores = db.fetchAllItems(StoreTables.pakNSaveStores)
    db.closeConnection()
    nwStoresClose = []
    psStoresClose = []
    for nwStore in newWorldStores:
        nwLat = float(nwStore[StoreTablesIndexes.latitude.value])
        nwLong = float(nwStore[StoreTablesIndexes.longitude.value])
        storeLocation = (nwLat, nwLong)
        if distance.geodesic(location, storeLocation).km <= radius:
            nwStoresClose.append(nwStore)

    for psStore in packNSaveStores:
        nwLat = float(psStore[StoreTablesIndexes.latitude.value])
        nwLong = float(psStore[StoreTablesIndexes.longitude.value])
        storeLocation = (nwLat, nwLong)
        if distance.geodesic(location, storeLocation).km <= radius:
            psStoresClose.append(psStore)

    return _parseStores(nwStoresClose, psStoresClose)


def searchForItems(query: str, newWorldIds: list[str], packNSaveIds: list[str]) -> ResponseType:
    db = Database()
    db.startConnection()
    items = db.fetchItemsByName(query, newWorldIds, packNSaveIds)
    newWorldItems = items[ItemTables.newWorld.value]
    packNSaveItems = items[ItemTables.pakNSave.value]
    countdownItems = items[ItemTables.countdown.value]
    itemsDictionary = _parseResponse(db, countdownItems, newWorldItems, packNSaveItems)
    outPutItemArray = []
    for item in sorted(itemsDictionary.values(), key=lambda itemGroup: sortByName(itemGroup, query), reverse=True):
        outPutItemArray.append(item)

    return {ItemTables.items.value: outPutItemArray}


def sortByName(items: list[dict[str, any]], query: str = "a"):
    ratios = 0
    for item in items:
        ratios += difflib.SequenceMatcher(None, item[SupermarketTableKeys.name.value], query).ratio()
    return ratios / (len(items))


def fetchPage(page: str, newWorldIds: list[str], packNSaveIds: list[str]) -> ResponseType:
    db = Database()
    db.startConnection()
    countdownItems = db.fetchCountdownItemsByPage(page)
    newWorldItems = db.fetchFoodStuffsItemsByPage(page, newWorldIds, ItemTables.newWorld)
    packNSaveItems = db.fetchFoodStuffsItemsByPage(page, packNSaveIds, ItemTables.pakNSave)
    itemsDictionary = _parseResponse(db, countdownItems, newWorldItems, packNSaveItems)
    outPutItemArray = []
    for item in sorted(itemsDictionary.values(), key=lambda itemGroups: sortByName(itemGroups), reverse=True):
        outPutItemArray.append(item)

    return {ItemTables.items.value: outPutItemArray}


def _parseResponse(db: Database,
                   countdownItems: list[tuple],
                   newWorldItems: list[tuple],
                   packNSaveItems: list[tuple]) -> dict[str, any]:
    concatIds = []
    for countDownItem in countdownItems:
        concatIds.append(countDownItem[SupermarketTableIndexes.itemId.value])

    for newWorldItem in newWorldItems:
        itemId = newWorldItem[SupermarketTableIndexes.itemId.value]
        if itemId not in concatIds:
            concatIds.append(itemId)

    for packNSaveItem in packNSaveItems:
        itemId = packNSaveItem[SupermarketTableIndexes.itemId.value]
        if itemId not in concatIds:
            concatIds.append(itemId)
    items = db.fetchItemsById(concatIds)
    db.closeConnection()

    itemsDict = {}
    for item in items:
        itemsDict[item[ItemsTableKeysIndexes.itemId.value]] = item

    itemsDictionary = {}

    for countDownItem in countdownItems:
        itemId = countDownItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(countDownItem, itemsDict, True)
        if not outPutItems:
            continue
        itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.countdown.value
            itemsDictionary[itemId].append(outPutItem)

    for newWorldItem in newWorldItems:
        itemId = newWorldItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(newWorldItem, itemsDict, False)
        if not outPutItems:
            continue

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.newWorld.value
            itemsDictionary[itemId].append(outPutItem)

    for packNSaveItem in packNSaveItems:
        itemId = packNSaveItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(packNSaveItem, itemsDict, False)
        if not outPutItems:
            continue

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.pakNSave.value
            itemsDictionary[itemId].append(outPutItem)

    return itemsDictionary


def _parseStores(newWorldStores: list[tuple], packNSaveStores: list[tuple]) -> dict[str, list[dict[str, str]]]:
    output = {
        StoreTables.newWorldStores.value: [],
        StoreTables.pakNSaveStores.value: []
    }
    for nwStore in newWorldStores:
        store = {}
        for index, key in zip(StoreTablesIndexes, StoreTablesKeys):
            store[key.value] = nwStore[index.value]
        output[StoreTables.newWorldStores.value].append(store)

    for psStore in packNSaveStores:
        store = {}
        for index, key in zip(StoreTablesIndexes, StoreTablesKeys):
            store[key.value] = psStore[index.value]
        output[StoreTables.pakNSaveStores.value].append(store)
    return output


def _parseItemsToDict(items: list[tuple]) -> list[dict[str, any]]:
    output = []
    for item in items:
        outPutItem = {}
        for index, key in enumerate(ItemsTableKeys):
            if key == ItemsTableKeys.category.value:
                outPutItem[key.value] = item[index].split("@")
            else:
                outPutItem[key.value] = item[index]
        output.append(outPutItem)
    return output


def _parseSuperMarketSingleItemToDict(supermarketItem: tuple,
                                      items: dict[str, any],
                                      isCountdown: bool) -> list[dict[str, any]]:
    outputArray = []
    for keyIndex in range(0, len(supermarketItem[SupermarketTableIndexes.price.value].split("@"))):
        itemId = supermarketItem[SupermarketTableIndexes.itemId.value]
        if itemId not in items.keys():
            continue
        itemDict = {}
        for index, key in enumerate(SupermarketTableKeys):
            if isCountdown and key == SupermarketTableKeys.supermarketId:
                continue
            if SupermarketTableKeys.itemId == key:
                itemDict[key.value] = supermarketItem[index]
                itemDict[ItemsTableKeys.category.value] = items[itemId][ItemsTableKeysIndexes.category.value]
                itemDict[ItemsTableKeys.brand.value] = items[itemId][ItemsTableKeysIndexes.brand.value]
                continue
            if SupermarketTableKeys.supermarketId == key or SupermarketTableKeys.page == key:
                itemDict[key.value] = supermarketItem[index]
                continue
            itemDict[key.value] = supermarketItem[index].split("@")[keyIndex]
        outputArray.append(itemDict)
    return outputArray


def _parseSuperMarketItemsToDict(supermarketItems: list[tuple],
                                 items: dict[str, any],
                                 isCountdown: bool) -> list[dict[str, any]]:
    output = []
    for item in supermarketItems:
        outPutItem = {}
        for index, key in enumerate(SupermarketTableKeys):
            if isCountdown and key == SupermarketTableKeys.supermarketId:
                continue
            if SupermarketTableKeys.itemId == key:
                outPutItem[key.value] = item[index]
                itemId = item[index]
                outPutItem[ItemsTableKeys.category.value] = items[itemId][ItemsTableKeysIndexes.category.value]
                outPutItem[ItemsTableKeys.brand.value] = items[itemId][ItemsTableKeysIndexes.brand.value]
                continue
            if SupermarketTableKeys.supermarketId == key:
                outPutItem[key.value] = item[index]
                continue
            outPutItem[key.value] = item[index].split("@")
        output.append(outPutItem)
    return output


def fetchCategories(categories: [str], newWorldIds: list[str], packNSaveIds: list[str]) -> ResponseType:
    db = Database()
    db.startConnection()
    items = db.fetchItemsByCategory(categories)
    itemIds = []
    itemsDict = {}
    for item in items:
        itemsDict[item[ItemsTableKeysIndexes.itemId.value]] = item
        itemIds.append(item[ItemsTableKeysIndexes.itemId.value])
    countdownItems = db.fetchCountdownItemsByIds(itemIds)
    newWorldItems = db.fetchFoodStuffsItemsIds(itemIds, newWorldIds, ItemTables.newWorld)
    packNSaveItems = db.fetchFoodStuffsItemsIds(itemIds, packNSaveIds, ItemTables.pakNSave)
    db.closeConnection()
    itemsDictionary = {}

    for countDownItem in countdownItems:
        itemId = countDownItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(countDownItem, itemsDict, True)
        itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.countdown.value
            itemsDictionary[itemId].append(outPutItem)

    for newWorldItem in newWorldItems:
        itemId = newWorldItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(newWorldItem, itemsDict, False)

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.newWorld.value
            itemsDictionary[itemId].append(outPutItem)

    for packNSaveItem in packNSaveItems:
        itemId = packNSaveItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(packNSaveItem, itemsDict, False)

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.pakNSave.value
            itemsDictionary[itemId].append(outPutItem)

    outPutItemArray = []
    for item in sorted(itemsDictionary.values(), key=lambda itemGroups: sortByName(itemGroups), reverse=True):
        outPutItemArray.append(item)

    return {ItemTables.items.value: outPutItemArray}
