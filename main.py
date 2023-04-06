import json
import uuid
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories
from SuperMarketsApis import OutputJsonKeys
from fuzzywuzzy import fuzz
from Database import ConcatcKeys


class SupportedStores(Enum):
    newWorld = "NewWorld"
    packNSave = "packNSave"
    countdown = "Countdown"


def createTables():
    db = Database()
    db.startConnection()
    db.createTable()
    db.printTables()
    db.closeConnection()


def dropTables():
    db = Database()
    db.startConnection()
    db.dropTable()
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
    itemsPerPage = 100
    page = 1
    values = []
    for index, item in enumerate(items.values()):
        itemValues = []
        for concatKey in ConcatcKeys:
            value = ''
            if type(item[concatKey.value]) == list:
                for vls in item[concatKey.value]:
                    value += vls + "@"
                value = value[:-1].replace("'", "")
            else:
                value = item[concatKey.value]
            itemValues.append(value)
        itemValues.append(f'{page}')
        values.append(itemValues)
        if index > 0 and index % itemsPerPage == 0:
            page += 1
    for item in values:
        print(item[-1])
    # db.startConnection()
    # db.insertItems(values)
    # db.closeConnection()


def _populateItem(items, dictionary, itemName, itemExists, brand, supermarket: SupportedStores):
    if not itemExists:
        items[itemName] = {}
        items[itemName][ConcatcKeys.newWorldItemNames.value] = []
        items[itemName][ConcatcKeys.newWorldPrices.value] = []
        items[itemName][ConcatcKeys.newWorldSizes.value] = []
        items[itemName][ConcatcKeys.newWorldphotoUrls.value] = []
        items[itemName][ConcatcKeys.countdownItemNames.value] = []
        items[itemName][ConcatcKeys.countdownPrices.value] = []
        items[itemName][ConcatcKeys.countdownSizes.value] = []
        items[itemName][ConcatcKeys.packNSaveSizes.value] = []
        items[itemName][ConcatcKeys.packNSaveItemNames.value] = []
        items[itemName][ConcatcKeys.packNSavePrices.value] = []
        items[itemName][ConcatcKeys.countdownphotoUrls.value] = []
        items[itemName][ConcatcKeys.packNSavephotoUrls.value] = []
        items[itemName][ConcatcKeys.category.value] = dictionary[OutputJsonKeys.category.value]
        items[itemName][ConcatcKeys.brand.value] = brand

    names = items[itemName][ConcatcKeys.countdownItemNames.value]
    prices = items[itemName][ConcatcKeys.countdownPrices.value]
    sizes = items[itemName][ConcatcKeys.countdownSizes.value]
    urls = items[itemName][ConcatcKeys.countdownphotoUrls.value]
    if supermarket == SupportedStores.newWorld:
        names = items[itemName][ConcatcKeys.newWorldItemNames.value]
        prices = items[itemName][ConcatcKeys.newWorldPrices.value]
        sizes = items[itemName][ConcatcKeys.newWorldSizes.value]
        urls = items[itemName][ConcatcKeys.newWorldphotoUrls.value]

    if supermarket == SupportedStores.packNSave:
        names = items[itemName][ConcatcKeys.packNSaveItemNames.value]
        prices = items[itemName][ConcatcKeys.packNSavePrices.value]
        sizes = items[itemName][ConcatcKeys.packNSaveSizes.value]
        urls = items[itemName][ConcatcKeys.packNSavephotoUrls.value]

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
    treshold = 80
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
    writeItemsToDB(items)
    # f = open("lol.txt", mode="w")
    # for key in sorted(items.keys(), key=lambda x: x.replace("-", "")):
    #     if items[key][ConcatcKeys.countdownItemNames.value] and items[key][ConcatcKeys.newWorldItemNames.value] and items[key][ConcatcKeys.packNSaveItemNames.value]:
    #         f.write(str(items[key]["brand"]) + "\n")
    #         f.write(str(items[key]["category"]) + "\n")
    #         f.write(key + "\n\n")
    #         f.write("cd" + str(items[key][ConcatcKeys.countdownItemNames.value]) + str(
    #             items[key][ConcatcKeys.countdownSizes.value]) + "\n")
    #         f.write("nw" + str(items[key][ConcatcKeys.newWorldItemNames.value]) + str(items[key][ConcatcKeys.newWorldSizes.value]) + "\n")
    #         f.write("ps" + str(items[key][ConcatcKeys.packNSaveItemNames.value]) + str(
    #             items[key][ConcatcKeys.packNSaveSizes.value]) + "\n")
    #         f.write("-" * 100 + "\n")
    #
    #     if items[key][ConcatcKeys.countdownItemNames.value] and items[key][ConcatcKeys.newWorldItemNames.value] and not items[key][ConcatcKeys.packNSaveItemNames.value]:
    #         f.write(str(items[key]["brand"]) + "\n")
    #         f.write(str(items[key]["category"]) + "\n")
    #         f.write(key + "\n\n")
    #         f.write("cd" + str(items[key][ConcatcKeys.countdownItemNames.value]) + str(
    #             items[key][ConcatcKeys.countdownSizes.value]) + "\n")
    #         f.write("nw" + str(items[key][ConcatcKeys.newWorldItemNames.value]) + str(
    #             items[key][ConcatcKeys.newWorldSizes.value]) + "\n")
    #         f.write("-" * 100 + "\n")
    #
    #     if items[key][ConcatcKeys.countdownItemNames.value] and not items[key][ConcatcKeys.newWorldItemNames.value] and items[key][ConcatcKeys.packNSaveItemNames.value]:
    #         f.write(str(items[key]["brand"]) + "\n")
    #         f.write(str(items[key]["category"]) + "\n")
    #         f.write(key + "\n\n")
    #         f.write("cd" + str(items[key][ConcatcKeys.countdownItemNames.value]) + str(
    #             items[key][ConcatcKeys.countdownSizes.value]) + "\n")
    #         f.write("ps" + str(items[key][ConcatcKeys.packNSaveItemNames.value]) + str(
    #             items[key][ConcatcKeys.packNSaveSizes.value]) + "\n")
    #         f.write("-" * 100 + "\n")
    #
    #     if not items[key][ConcatcKeys.countdownItemNames.value] and items[key][ConcatcKeys.newWorldItemNames.value] and items[key][ConcatcKeys.packNSaveItemNames.value]:
    #         f.write(str(items[key]["brand"]) + "\n")
    #         f.write(str(items[key]["category"]) + "\n")
    #         f.write(key + "\n\n")
    #         f.write("cd" + str(items[key][ConcatcKeys.newWorldItemNames.value]) + str(
    #             items[key][ConcatcKeys.newWorldSizes.value]) + "\n")
    #         f.write("ps" + str(items[key][ConcatcKeys.packNSaveItemNames.value]) + str(
    #             items[key][ConcatcKeys.packNSaveSizes.value]) + "\n")
    #         f.write("-" * 100 + "\n")
    # f.close()

    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()

# dropTables()
# createTables()
# clusterData()
db = Database()
db.startConnection()
print(db.fetchItemsByCategory("drink"))
db.closeConnection()