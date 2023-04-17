from Database import Database
from Database import ItemsTableKeys, SupermarketTableKeys, ItemTables, \
    StoreTables, StoreTablesKeys, StoreTablesIndexes, ItemsTableKeysIndexes
from geopy import distance


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
    items = db.fetchPage(page)
    itemIds = []
    itemsDict = {}
    for item in items:
        itemsDict[item[ItemsTableKeysIndexes.itemId.value]] = item
        itemIds.append(item[ItemsTableKeysIndexes.itemId.value])
    countDown = db.fetchCountdownItems(itemIds)
    nwItems = db.fetchFoodStuffsItems(itemIds, newWorldIds, ItemTables.newWorld)
    psItems = db.fetchFoodStuffsItems(itemIds, packNSaveIds, ItemTables.pakNSave)
    db.closeConnection()
    return {
        ItemTables.newWorld.value: _parseSuperMarketItemsToDict(nwItems, itemsDict, False),
        ItemTables.pakNSave.value: _parseSuperMarketItemsToDict(psItems, itemsDict, False),
        ItemTables.countdown.value: _parseSuperMarketItemsToDict(countDown, itemsDict, True)
    }


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
    countDown = db.fetchCountdownItems(itemIds)
    nwItems = db.fetchFoodStuffsItems(itemIds, newWorldIds, ItemTables.newWorld)
    psItems = db.fetchFoodStuffsItems(itemIds, packNSaveIds, ItemTables.pakNSave)
    db.closeConnection()
    return {
        ItemTables.newWorld.value: _parseSuperMarketItemsToDict(nwItems, itemsDict, False),
        ItemTables.pakNSave.value: _parseSuperMarketItemsToDict(psItems, itemsDict, False),
        ItemTables.countdown.value: _parseSuperMarketItemsToDict(countDown, itemsDict, True)
    }
