from Database import Database
from Database import ItemsTableKeys, SupermarketTableKeys, SupermarketTableIndexes, ItemTables, \
    StoreTables, StoreTablesKeys, StoreTablesIndexes, ItemsTableKeysIndexes
from geopy import distance
import re


def fetchStores(lat: str, long: str, radius: str):
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


def fetchItems(query, newWorldIds, packNSaveIds):
    db = Database()
    db.startConnection()
    items = db.fetchItemsByName(query, newWorldIds, packNSaveIds)
    nwItems = items[ItemTables.newWorld.value]
    itemsDict = items[ItemTables.items.value]
    psItems = items[ItemTables.pakNSave.value]
    countDown = items[ItemTables.countdown.value]
    db.closeConnection()
    return {
        ItemTables.newWorld.value: _parseSuperMarketItemsToDict(nwItems, itemsDict, False),
        ItemTables.pakNSave.value: _parseSuperMarketItemsToDict(psItems, itemsDict, False),
        ItemTables.countdown.value: _parseSuperMarketItemsToDict(countDown, itemsDict, True)
    }


def fetchPage(page, newWorldIds, packNSaveIds):
    db = Database()
    db.startConnection()
    countDown = db.fetchCountdownItemsByPage(page)
    nwItems = db.fetchFoodStuffsItemsByPage(page, newWorldIds, ItemTables.newWorld)
    psItems = db.fetchFoodStuffsItemsByPage(page, packNSaveIds, ItemTables.pakNSave)
    concatIds = []
    for countDownItem in countDown:
        concatIds.append(countDownItem[SupermarketTableIndexes.itemId.value])

    for newWorldItem in nwItems:
        itemId = newWorldItem[SupermarketTableIndexes.itemId.value]
        if itemId not in concatIds:
            concatIds.append(itemId)

    for packNSaveItem in psItems:
        itemId = packNSaveItem[SupermarketTableIndexes.itemId.value]
        if itemId not in concatIds:
            concatIds.append(itemId)
    items = db.fetchItemsById(concatIds)

    itemIds = []
    itemsDict = {}
    for item in items:
        itemsDict[item[ItemsTableKeysIndexes.itemId.value]] = item
        itemIds.append(item[ItemsTableKeysIndexes.itemId.value])

    itemsDictionary = {}

    for countDownItem in countDown:
        itemId = countDownItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(countDownItem, itemsDict, True)
        itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.countdown.value
            itemsDictionary[itemId].append(outPutItem)

    for newWorldItem in nwItems:
        itemId = newWorldItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(newWorldItem, itemsDict, False)

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.newWorld.value
            itemsDictionary[itemId].append(outPutItem)

    for packNSaveItem in psItems:
        itemId = packNSaveItem[SupermarketTableIndexes.itemId.value]
        outPutItems = _parseSuperMarketSingleItemToDict(packNSaveItem, itemsDict, False)

        if itemId not in itemsDictionary.keys():
            itemsDictionary[itemId] = []
        for outPutItem in outPutItems:
            outPutItem["supermarket"] = ItemTables.pakNSave.value
            itemsDictionary[itemId].append(outPutItem)

    outPutItemArray = []
    for item in sorted(itemsDictionary.values(), key=lambda x: sortingKey(x[0])):
        outPutItemArray.append(item)
    db.closeConnection()

    return {ItemTables.items.value: outPutItemArray}


def sortingKey(item) -> str:
    nameString = item[SupermarketTableKeys.name.value]
    names = []
    for name in nameString.split("@"):
        numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
        for number in numbers:
            name = name.replace(number, "")
        names.append(name)
    names = sorted(names)
    return names[0]


def _parseStores(newWorldStores, packNSaveStores) -> dict:
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


def _parseSuperMarketSingleItemToDict(supermarketItem, items, isCountdown) -> list:
    outputArray = []
    for keyIndex in range(0, len(supermarketItem[SupermarketTableIndexes.price.value].split("@"))):
        itemDict = {}
        for index, key in enumerate(SupermarketTableKeys):
            if isCountdown and key == SupermarketTableKeys.supermarketId:
                continue
            if SupermarketTableKeys.itemId == key:
                itemDict[key.value] = supermarketItem[index]
                itemId = supermarketItem[index]
                itemDict[ItemsTableKeys.category.value] = items[itemId][ItemsTableKeysIndexes.category.value]
                itemDict[ItemsTableKeys.brand.value] = items[itemId][ItemsTableKeysIndexes.brand.value]
                continue
            if SupermarketTableKeys.supermarketId == key or SupermarketTableKeys.page == key:
                itemDict[key.value] = supermarketItem[index]
                continue
            itemDict[key.value] = supermarketItem[index].split("@")[keyIndex]
        outputArray.append(itemDict)
    return outputArray


def _parseSuperMarketItemsToDict(supermarketItems, items, isCountdown) -> list:
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


def fetchCategories(categories: [str], newWorldIds, packNSaveIds):
    db = Database()
    db.startConnection()
    items = db.fetchItemsByCategory(categories)
    itemIds = []
    itemsDict = {}
    for item in items:
        itemsDict[item[ItemsTableKeysIndexes.itemId.value]] = item
        itemIds.append(item[ItemsTableKeysIndexes.itemId.value])
    countDown = db.fetchCountdownItemsByIds(itemIds)
    nwItems = db.fetchFoodStuffsItemsIds(itemIds, newWorldIds, ItemTables.newWorld)
    psItems = db.fetchFoodStuffsItemsIds(itemIds, packNSaveIds, ItemTables.pakNSave)
    db.closeConnection()
    return {
        ItemTables.newWorld.value: _parseSuperMarketItemsToDict(nwItems, itemsDict, False),
        ItemTables.pakNSave.value: _parseSuperMarketItemsToDict(psItems, itemsDict, False),
        ItemTables.countdown.value: _parseSuperMarketItemsToDict(countDown, itemsDict, True)
    }
