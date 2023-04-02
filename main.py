import json
import uuid
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories


class SupportedStores(Enum):
    newWorld = "NewWorld"
    PackNSave = "packNSave"
    countdown = "Countdown"


class ConcatcKeys(Enum):
    newWorldItems = "newWorldItems"
    packNSaveItems = "PackNSaveItems"
    countdownItems = "countdownItems"
    newWorldPrice = "newWorldPrice"
    packNSavePrice = "PackNSavePrice"
    countdownPrice = "countdownPrice"
    newWorldPhotoUrls = "newWorldPhotoUrls"
    packNSavePhotoUrls = "packNSavePhotoUrls"
    countdownPhotoUrls = "countdownPhotoUrls"
    category = "category"
    brand = "brand"


def createTables():
    db = Database()
    db.startConnection()
    for store in SupportedStores:
        db.createTable(tableName=store.value, tableParameters=["ID VARCHAR(255)",
                                                               "itemName LONGTEXT",
                                                               "itemPrice LONGTEXT",
                                                               "itemUrls LONGTEXT",
                                                               "itemCategory LONGTEXT",
                                                               "itemBrand VARCHAR(255)"])
    db.printTables()
    db.closeConnection()


def dropTables():
    db = Database()
    db.startConnection()
    for store in SupportedStores:
        db.dropTable(store.value)
    db.printTables()
    db.closeConnection()


def fetchData():
    api = Apis()
    api.fetchFoodStuffItems(SuperMarketAbbreviation.newWorld)
    api.fetchFoodStuffItems(SuperMarketAbbreviation.packNSave)
    api.fetchCountdownItems()


def concatCategory(oldCategory: str, newCategoryString: str) -> str:
    newCategories = newCategoryString.split("@")
    for newCategory in newCategories:
        if newCategory not in oldCategory:
            oldCategory += '@' + newCategory
    return oldCategory


def writeItemsToDB(items):
    db = Database()
    countDown = {}
    newWorld = {}
    packNSave = {}
    for item in items.values():
        id = uuid.uuid1()
        if item[ConcatcKeys.countdownItems.value]:
            countDown[id] = {}
            countDownItem = countDown[id]
            countDownItem["name"] = item[ConcatcKeys.countdownItems.value]
            countDownItem["price"] = item[ConcatcKeys.countdownPrice.value]
            countDownItem["photoUrls"] = item[ConcatcKeys.countdownPhotoUrls.value]
            countDownItem["brand"] = item[ConcatcKeys.brand.value]
            countDownItem["category"] = item[ConcatcKeys.category.value]
        if item[ConcatcKeys.newWorldItems.value]:
            newWorld[id] = {}
            newWorldItem = newWorld[id]
            newWorldItem["name"] = item[ConcatcKeys.newWorldItems.value]
            newWorldItem["price"] = item[ConcatcKeys.newWorldPrice.value]
            newWorldItem["photoUrls"] = item[ConcatcKeys.newWorldPhotoUrls.value]
            newWorldItem["brand"] = item[ConcatcKeys.brand.value]
            newWorldItem["category"] = item[ConcatcKeys.category.value]
        if item[ConcatcKeys.packNSaveItems.value]:
            packNSave[id] = {}
            packNSaveItem = packNSave[id]
            packNSaveItem["name"] = item[ConcatcKeys.packNSaveItems.value]
            packNSaveItem["price"] = item[ConcatcKeys.packNSavePrice.value]
            packNSaveItem["photoUrls"] = item[ConcatcKeys.packNSavePhotoUrls.value]
            packNSaveItem["brand"] = item[ConcatcKeys.brand.value]
            packNSaveItem["category"] = item[ConcatcKeys.category.value]
    db.startConnection()
    parameters = []
    for newWorldItemKey in newWorld.keys():
        id = str(newWorldItemKey)
        values = newWorld[newWorldItemKey]
        name = ''
        for names in values["name"]:
            name += names + "@"
        name = name[:-1].replace("'", "")
        price = ''
        for prices in values["price"]:
            price += prices + "@"
        price = price[:-1]
        photoUrls = ''
        for urls in values["photoUrls"]:
            photoUrls += urls + "@"
        photoUrls = photoUrls[:-1]
        category = f'{values["category"]}'
        brand = f'{values["brand"]}'

        parameters.append((id,
                           name,
                           price,
                           photoUrls,
                           category,
                           brand))
    db.insertItems(SupportedStores.newWorld.value, parameters)
    itms = db.fetchItems(SupportedStores.newWorld.value)
    for item in itms:
        print(item[1])
    db.closeConnection()

def writeCountDownItem(items, dictionary, itemName, itemExists, brand):
    if itemExists:
        if dictionary["name"] in items[itemName][ConcatcKeys.countdownItems.value]:
            return
        items[itemName][ConcatcKeys.countdownItems.value].append(dictionary["name"])
        items[itemName][ConcatcKeys.countdownPrice.value].append(dictionary["price"])
        items[itemName][ConcatcKeys.countdownPhotoUrls.value].append(dictionary["photoUrl"])
        items[itemName][ConcatcKeys.category.value] = concatCategory(
            items[itemName][ConcatcKeys.category.value], dictionary["category"])
    else:
        items[itemName] = {}
        items[itemName][ConcatcKeys.countdownItems.value] = [dictionary["name"]]
        items[itemName][ConcatcKeys.countdownPrice.value] = [dictionary["price"]]
        items[itemName][ConcatcKeys.newWorldPrice.value] = []
        items[itemName][ConcatcKeys.newWorldItems.value] = []
        items[itemName][ConcatcKeys.packNSaveItems.value] = []
        items[itemName][ConcatcKeys.packNSavePrice.value] = []
        items[itemName][ConcatcKeys.newWorldPhotoUrls.value] = []
        items[itemName][ConcatcKeys.packNSavePhotoUrls.value] = []
        items[itemName][ConcatcKeys.countdownPhotoUrls.value] = [dictionary["photoUrl"]]
        items[itemName][ConcatcKeys.category.value] = dictionary["category"]
        items[itemName][ConcatcKeys.brand.value] = brand


def writeNewWorldItem(items, dictionary, itemName, itemExists, brand):
    if itemExists:
        if dictionary["name"] in items[itemName][ConcatcKeys.newWorldItems.value]:
            return
        items[itemName][ConcatcKeys.newWorldItems.value].append(dictionary["name"])
        items[itemName][ConcatcKeys.newWorldPrice.value].append(dictionary["price"])
        items[itemName][ConcatcKeys.newWorldPhotoUrls.value].append(dictionary["photoUrl"])
        items[itemName][ConcatcKeys.category.value] = concatCategory(
            items[itemName][ConcatcKeys.category.value], dictionary["category"])
    else:
        items[itemName] = {}
        items[itemName][ConcatcKeys.newWorldItems.value] = [dictionary["name"]]
        items[itemName][ConcatcKeys.newWorldPrice.value] = [dictionary["price"]]
        items[itemName][ConcatcKeys.newWorldPhotoUrls.value] = [dictionary["photoUrl"]]
        items[itemName][ConcatcKeys.countdownItems.value] = []
        items[itemName][ConcatcKeys.countdownPrice.value] = []
        items[itemName][ConcatcKeys.packNSaveItems.value] = []
        items[itemName][ConcatcKeys.packNSavePrice.value] = []
        items[itemName][ConcatcKeys.countdownPhotoUrls.value] = []
        items[itemName][ConcatcKeys.packNSavePhotoUrls.value] = []
        items[itemName][ConcatcKeys.category.value] = dictionary["category"]
        items[itemName][ConcatcKeys.brand.value] = brand


def writePackNSaveItem(items, dictionary, itemName, itemExists, brand):
    if itemExists:
        if dictionary["name"] in items[itemName][ConcatcKeys.packNSaveItems.value]:
            return
        items[itemName][ConcatcKeys.packNSaveItems.value].append(dictionary["name"])
        items[itemName][ConcatcKeys.packNSavePrice.value].append(dictionary["price"])
        items[itemName][ConcatcKeys.packNSavePhotoUrls.value].append(dictionary["photoUrl"])
        items[itemName][ConcatcKeys.category.value] = concatCategory(
            items[itemName][ConcatcKeys.category.value], dictionary["category"])
    else:
        items[itemName] = {}
        items[itemName][ConcatcKeys.packNSaveItems.value] = [dictionary["name"]]
        items[itemName][ConcatcKeys.packNSavePrice.value] = [dictionary["price"]]
        items[itemName][ConcatcKeys.packNSavePhotoUrls.value] = [dictionary["photoUrl"]]
        items[itemName][ConcatcKeys.countdownItems.value] = []
        items[itemName][ConcatcKeys.countdownPrice.value] = []
        items[itemName][ConcatcKeys.newWorldItems.value] = []
        items[itemName][ConcatcKeys.newWorldPrice.value] = []
        items[itemName][ConcatcKeys.newWorldPhotoUrls.value] = []
        items[itemName][ConcatcKeys.countdownPhotoUrls.value] = []
        items[itemName][ConcatcKeys.category.value] = dictionary["category"]
        items[itemName][ConcatcKeys.brand.value] = brand


def clusterData():
    countdownFile = open("countDownData.json")
    newWorldFile = open("newWorldData.json")
    packNSaveFile = open("packNSaveData.json")

    stopWordsFile = open("stopWords.json")
    stopWordsString = stopWordsFile.read()
    stopWordsFile.close()
    stopSet = json.loads(stopWordsString)["nonKeyWords"]

    coutdownString = countdownFile.read()
    newWorldString = newWorldFile.read()
    packNSaveString = packNSaveFile.read()

    countdownDict = json.loads(coutdownString)
    newWorldDict = json.loads(newWorldString)
    packNSaveDict = json.loads(packNSaveString)

    newWorldKeyMap = {}
    packNSaveKeyMap = {}
    newWorldKeys = []
    packNSaveKeys = []
    countdownKeys = []

    for key in newWorldDict.keys():
        k = finalCategories.transformToKey(key)
        newWorldKeys.append(k)
        newWorldKeyMap[k] = key

    for key in packNSaveDict.keys():
        k = finalCategories.transformToKey(key)
        packNSaveKeys.append(k)
        packNSaveKeyMap[k] = key

    countdownKeyMap = {}
    for key in countdownDict.keys():
        k = finalCategories.transformToKey(key)
        countdownKeys.append(k)
        countdownKeyMap[k] = key

    items = {}
    for key in countdownDict.keys():
        brand = countdownDict[key]
        ckm = finalCategories.transformToKey(key)
        countdownKeys.remove(ckm)
        for countDownItem in brand:
            countdownName = finalCategories.transformItem(countDownItem["name"], stopSet)
            writeCountDownItem(items, countDownItem, countdownName, countdownName in items, key)

            if ckm in newWorldKeyMap:
                for newWorldItem in newWorldDict[newWorldKeyMap[ckm]]:
                    newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
                    itemExists = newWorldName in countdownName or \
                                 countdownName in newWorldName or \
                                 countdownName == newWorldName or \
                                 countdownName in items or \
                                 newWorldName in items
                    name = newWorldName
                    if itemExists:
                        name = countdownName
                    writeNewWorldItem(items, newWorldItem, name, itemExists, key)
            if ckm in newWorldKeys:
                newWorldKeys.remove(ckm)

            if ckm in packNSaveKeyMap:
                for packNSaveItem in packNSaveDict[packNSaveKeyMap[ckm]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem["name"], stopSet)
                    itemExists = pakNSaveName in countdownName or \
                                 countdownName in pakNSaveName or \
                                 countdownName == pakNSaveName or \
                                 countdownName in items or \
                                 pakNSaveName in items
                    name = pakNSaveName
                    if itemExists:
                        name = countdownName
                    writePackNSaveItem(items, packNSaveItem, name, itemExists, key)
            if ckm in packNSaveKeys:
                packNSaveKeys.remove(ckm)

    for key in newWorldKeyMap.keys():
        if key in packNSaveKeyMap and key not in items.keys():
            for newWorldItem in newWorldDict[newWorldKeyMap[key]]:
                newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
                writeNewWorldItem(items, newWorldItem, newWorldName, newWorldName in items, newWorldKeyMap[key])

                for packNSaveItem in packNSaveDict[packNSaveKeyMap[key]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem["name"], stopSet)
                    itemExists = newWorldName in pakNSaveName or \
                                 pakNSaveName in newWorldName or \
                                 pakNSaveName == newWorldName or \
                                 pakNSaveName in items or \
                                 newWorldName in items
                    name = pakNSaveName
                    if itemExists:
                        name = newWorldName
                    writePackNSaveItem(items, packNSaveItem, name, itemExists, newWorldKeyMap[key])
            if key in packNSaveKeys:
                packNSaveKeys.remove(key)
            if key in newWorldKeys:
                newWorldKeys.remove(key)

    for ck in countdownKeys:
        for countDownItem in countdownDict[countdownKeyMap[ck]]:
            countdownName = finalCategories.transformItem(countDownItem["name"], stopSet)
            writeCountDownItem(items, countDownItem, countdownName, countdownName in items, countdownKeyMap[ck])

    for nwk in newWorldKeys:
        for newWorldItem in newWorldDict[newWorldKeyMap[nwk]]:
            newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
            writeNewWorldItem(items, newWorldItem, newWorldName, newWorldName in items, newWorldKeyMap[nwk])

    for psk in packNSaveKeys:
        for pakNSaveItem in packNSaveDict[packNSaveKeyMap[psk]]:
            pakNSaveName = finalCategories.transformItem(pakNSaveItem["name"], stopSet)
            writePackNSaveItem(items, pakNSaveItem, pakNSaveName, pakNSaveName in items, packNSaveKeyMap[psk])
    writeItemsToDB(items)

    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()

dropTables()
createTables()
clusterData()