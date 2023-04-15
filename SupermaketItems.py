from Database import Database
from Database import ItemsTableKeys, SupermarketTableKeys, ItemTables, StoreTables, StoreTablesKeys, StoreTablesIndexes
from geopy import distance
def fetchStores(lat: str, long: str, radius: str):
    radius = float(radius)
    location = (float(lat), float(long))
    db = Database()
    db.startConnection()
    newWorldStores = db.fetchAllItems(StoreTables.newWorldStores)
    packNSaveStores = db.fetchAllItems(StoreTables.pakNSaveStores)
    nwStoresClose = []
    psStoresClose = []
    for nwStore in newWorldStores:
        nwLat = float(nwStore[StoreTablesIndexes.latitude.value])
        nwLong = float(nwStore[StoreTablesIndexes.longitude.value])
        storeLocation = (nwLat, nwLong)
        print(distance.geodesic(location, storeLocation).km)
        if distance.geodesic(location, storeLocation).km <= radius:
            nwStoresClose.append(nwStore)

    for psStore in packNSaveStores:
        nwLat = float(psStore[StoreTablesIndexes.latitude.value])
        nwLong = float(psStore[StoreTablesIndexes.longitude.value])
        storeLocation = (nwLat, nwLong)
        if distance.geodesic(location, storeLocation).km <= radius:
            psStoresClose.append(psStore)

    return _parseStores(nwStoresClose, psStoresClose)


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
