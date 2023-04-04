import json
import uuid
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories
from SuperMarketsApis import OutputJsonKeys
from fuzzywuzzy import fuzz


class SupportedStores(Enum):
    newWorld = "NewWorld"
    packNSave = "packNSave"
    countdown = "Countdown"

class ConcatcKeys(Enum):
    newWorldItems = "newWorldItems"
    packNSaveItems = "PackNSaveItems"
    countdownItems = "countdownItems"
    newWorldPrice = "newWorldPrice"
    packNSavePrice = "PackNSavePrice"
    countdownPrice = "countdownPrice"
    newWorldphotoUrl = "newWorldphotoUrl"
    packNSavephotoUrl = "packNSavephotoUrl"
    countdownphotoUrl = "countdownphotoUrl"
    newWorldSize = "newWorldSize"
    packNSaveSize = "packNSaveSize"
    countdownSize = "countdownSize"
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
            countDownItem[OutputJsonKeys.name.value] = item[ConcatcKeys.countdownItems.value]
            countDownItem[OutputJsonKeys.price.value] = item[ConcatcKeys.countdownPrice.value]
            countDownItem[OutputJsonKeys.photoUrl.value] = item[ConcatcKeys.countdownphotoUrl.value]
            countDownItem[OutputJsonKeys.brand.value] = item[ConcatcKeys.brand.value]
            countDownItem[OutputJsonKeys.category.value] = item[ConcatcKeys.category.value]
        if item[ConcatcKeys.newWorldItems.value]:
            newWorld[id] = {}
            newWorldItem = newWorld[id]
            newWorldItem[OutputJsonKeys.name.value] = item[ConcatcKeys.newWorldItems.value]
            newWorldItem[OutputJsonKeys.price.value] = item[ConcatcKeys.newWorldPrice.value]
            newWorldItem[OutputJsonKeys.photoUrl.value] = item[ConcatcKeys.newWorldphotoUrl.value]
            newWorldItem[OutputJsonKeys.brand.value] = item[ConcatcKeys.brand.value]
            newWorldItem[OutputJsonKeys.category.value] = item[ConcatcKeys.category.value]
        if item[ConcatcKeys.packNSaveItems.value]:
            packNSave[id] = {}
            packNSaveItem = packNSave[id]
            packNSaveItem[OutputJsonKeys.name.value] = item[ConcatcKeys.packNSaveItems.value]
            packNSaveItem[OutputJsonKeys.price.value] = item[ConcatcKeys.packNSavePrice.value]
            packNSaveItem[OutputJsonKeys.photoUrl.value] = item[ConcatcKeys.packNSavephotoUrl.value]
            packNSaveItem[OutputJsonKeys.brand.value] = item[ConcatcKeys.brand.value]
            packNSaveItem[OutputJsonKeys.category.value] = item[ConcatcKeys.category.value]
    db.startConnection()
    parameters = []
    for newWorldItemKey in newWorld.keys():
        id = str(newWorldItemKey)
        if newWorldItemKey in countDown.keys():
            print(newWorld[newWorldItemKey])
            print(countDown[newWorldItemKey])
        values = newWorld[newWorldItemKey]
        name = ''
        for names in values[OutputJsonKeys.name.value]:
            name += names + "@"
        name = name[:-1].replace("'", "")
        price = ''
        for prices in values[OutputJsonKeys.price.value]:
            price += prices + "@"
        price = price[:-1]
        photoUrl = ''
        for urls in values[OutputJsonKeys.photoUrl.value]:
            photoUrl += urls + "@"
        photoUrl = photoUrl[:-1]
        category = f'{values[OutputJsonKeys.category.value]}'
        brand = f'{values[OutputJsonKeys.brand.value]}'

        parameters.append((id,
                           name,
                           price,
                           photoUrl,
                           category,
                           brand))
    db.insertItems(SupportedStores.newWorld.value, parameters)
    itms = db.fetchItems(SupportedStores.newWorld.value)
    for item in itms:
        print(item[1], item[2], item[3], item[4], item[5])
    db.closeConnection()


def _populateItem(items, dictionary, itemName, itemExists, brand, supermarket: SupportedStores):
    if not itemExists:
        items[itemName] = {}
        items[itemName][ConcatcKeys.newWorldItems.value] = []
        items[itemName][ConcatcKeys.newWorldPrice.value] = []
        items[itemName][ConcatcKeys.newWorldSize.value] = []
        items[itemName][ConcatcKeys.newWorldphotoUrl.value] = []
        items[itemName][ConcatcKeys.countdownItems.value] = []
        items[itemName][ConcatcKeys.countdownPrice.value] = []
        items[itemName][ConcatcKeys.countdownSize.value] = []
        items[itemName][ConcatcKeys.packNSaveSize.value] = []
        items[itemName][ConcatcKeys.packNSaveItems.value] = []
        items[itemName][ConcatcKeys.packNSavePrice.value] = []
        items[itemName][ConcatcKeys.countdownphotoUrl.value] = []
        items[itemName][ConcatcKeys.packNSavephotoUrl.value] = []
        items[itemName][ConcatcKeys.category.value] = dictionary[OutputJsonKeys.category.value]
        items[itemName][ConcatcKeys.brand.value] = brand

    names = items[itemName][ConcatcKeys.countdownItems.value]
    prices = items[itemName][ConcatcKeys.countdownPrice.value]
    sizes = items[itemName][ConcatcKeys.countdownSize.value]
    urls = items[itemName][ConcatcKeys.countdownphotoUrl.value]
    if supermarket == SupportedStores.newWorld:
        names = items[itemName][ConcatcKeys.newWorldItems.value]
        prices = items[itemName][ConcatcKeys.newWorldPrice.value]
        sizes = items[itemName][ConcatcKeys.newWorldSize.value]
        urls = items[itemName][ConcatcKeys.newWorldphotoUrl.value]

    if supermarket == SupportedStores.packNSave:
        names = items[itemName][ConcatcKeys.packNSaveItems.value]
        prices = items[itemName][ConcatcKeys.packNSavePrice.value]
        sizes = items[itemName][ConcatcKeys.packNSaveSize.value]
        urls = items[itemName][ConcatcKeys.packNSavephotoUrl.value]

    for index, item in enumerate(names):
        if item == dictionary[OutputJsonKeys.name.value] and dictionary["size"] == sizes[index]:
            return

    names.append(dictionary[OutputJsonKeys.name.value])
    prices.append(dictionary[OutputJsonKeys.price.value])
    sizes.append(dictionary["size"])
    urls.append(dictionary["photoUrl"])
    items[itemName][ConcatcKeys.category.value] = concatCategory(
        items[itemName][ConcatcKeys.category.value], dictionary[OutputJsonKeys.category.value])


def clusterData():
    treshold = 90
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
            countdownName = finalCategories.transformItem(countDownItem[OutputJsonKeys.name.value], stopSet)

            _populateItem(items, countDownItem, countdownName, countdownName in items, key, SupportedStores.countdown)

            if ckm in newWorldKeyMap:
                for newWorldItem in newWorldDict[newWorldKeyMap[ckm]]:
                    newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)

                    itemExists = fuzz.partial_ratio(newWorldName, countdownName) > treshold and \
                                 (countdownName in items or
                                  newWorldName in items)
                    name = newWorldName
                    if itemExists:
                        name = countdownName
                    _populateItem(items, newWorldItem, name, itemExists, key, SupportedStores.newWorld)
            if ckm in newWorldKeys:
                newWorldKeys.remove(ckm)

            if ckm in packNSaveKeyMap:
                for packNSaveItem in packNSaveDict[packNSaveKeyMap[ckm]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem[OutputJsonKeys.name.value], stopSet)

                    itemExists = fuzz.partial_ratio(pakNSaveName, countdownName) > treshold and \
                                 (countdownName in items or
                                  pakNSaveName in items)
                    name = pakNSaveName
                    if itemExists:
                        name = countdownName
                    _populateItem(items, packNSaveItem, name, itemExists, key, SupportedStores.packNSave)
            if ckm in packNSaveKeys:
                packNSaveKeys.remove(ckm)

    for key in newWorldKeyMap.keys():
        if key in packNSaveKeyMap and key not in items.keys():
            for newWorldItem in newWorldDict[newWorldKeyMap[key]]:
                newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)

                _populateItem(items, newWorldItem, newWorldName, newWorldName in items, newWorldKeyMap[key],
                              SupportedStores.newWorld)

                for packNSaveItem in packNSaveDict[packNSaveKeyMap[key]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem[OutputJsonKeys.name.value], stopSet)

                    itemExists = fuzz.partial_ratio(pakNSaveName, newWorldName) > treshold and \
                                 (pakNSaveName in items or
                                  newWorldName in items)
                    name = pakNSaveName
                    if itemExists:
                        name = newWorldName
                    _populateItem(items, packNSaveItem, name, itemExists, newWorldKeyMap[key],
                                  SupportedStores.packNSave)
            if key in packNSaveKeys:
                packNSaveKeys.remove(key)
            if key in newWorldKeys:
                newWorldKeys.remove(key)

    for ck in countdownKeys:
        for countDownItem in countdownDict[countdownKeyMap[ck]]:
            countdownName = finalCategories.transformItem(countDownItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, countDownItem, countdownName, countdownName in items, countdownKeyMap[ck],
                          SupportedStores.countdown)

    for nwk in newWorldKeys:
        for newWorldItem in newWorldDict[newWorldKeyMap[nwk]]:
            newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, newWorldItem, newWorldName, newWorldName in items, newWorldKeyMap[nwk],
                          SupportedStores.newWorld)

    for psk in packNSaveKeys:
        for pakNSaveItem in packNSaveDict[packNSaveKeyMap[psk]]:
            pakNSaveName = finalCategories.transformItem(pakNSaveItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, pakNSaveItem, pakNSaveName, pakNSaveName in items, packNSaveKeyMap[psk],
                          SupportedStores.packNSave)
    f = open("lol.txt", mode="w")
    for key in sorted(items.keys(), key=lambda x: x.replace("-", "")):
        if items[key][ConcatcKeys.countdownItems.value] and items[key][ConcatcKeys.newWorldItems.value] and items[key][ConcatcKeys.packNSaveItems.value]:
            print(items[key])
            f.write(key + "\n\n")
            f.write("cd" + str(items[key][ConcatcKeys.countdownItems.value]) + str(
                items[key][ConcatcKeys.countdownSize.value]) + "\n")
            f.write("cd" + str(items[key][ConcatcKeys.newWorldItems.value]) + str(
                items[key][ConcatcKeys.newWorldSize.value]) + "\n")
            f.write("cd" + str(items[key][ConcatcKeys.packNSaveItems.value]) + str(
                items[key][ConcatcKeys.packNSaveSize.value]) + "\n")
            f.write("-" * 100 + "\n")

        if items[key][ConcatcKeys.countdownItems.value] and items[key][ConcatcKeys.newWorldItems.value] and not items[key][ConcatcKeys.packNSaveItems.value]:
            print(items[key])
            f.write(key + "\n\n")
            f.write("cd" + str(items[key][ConcatcKeys.countdownItems.value]) + str(
                items[key][ConcatcKeys.countdownSize.value]) + "\n")
            f.write("cd" + str(items[key][ConcatcKeys.newWorldItems.value]) + str(
                items[key][ConcatcKeys.newWorldSize.value]) + "\n")
            f.write("-" * 100 + "\n")

        if items[key][ConcatcKeys.countdownItems.value] and not items[key][ConcatcKeys.newWorldItems.value] and items[key][ConcatcKeys.packNSaveItems.value]:
            print(items[key])
            f.write(key + "\n\n")
            f.write("cd" + str(items[key][ConcatcKeys.countdownItems.value]) + str(
                items[key][ConcatcKeys.countdownSize.value]) + "\n")
            f.write("cd" + str(items[key][ConcatcKeys.packNSaveItems.value]) + str(
                items[key][ConcatcKeys.packNSaveSize.value]) + "\n")
            f.write("-" * 100 + "\n")

        if not items[key][ConcatcKeys.countdownItems.value] and items[key][ConcatcKeys.newWorldItems.value] and items[key][ConcatcKeys.packNSaveItems.value]:
            print(items[key])
            f.write(key + "\n\n")
            f.write("cd" + str(items[key][ConcatcKeys.newWorldItems.value]) + str(
                items[key][ConcatcKeys.newWorldSize.value]) + "\n")
            f.write("cd" + str(items[key][ConcatcKeys.packNSaveItems.value]) + str(
                items[key][ConcatcKeys.packNSaveSize.value]) + "\n")
            f.write("-" * 100 + "\n")
    f.close()

    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()


clusterData()
