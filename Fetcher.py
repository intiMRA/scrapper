import json
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories
from SuperMarketsApis import OutputJsonKeys
from fuzzywuzzy import fuzz
from Database import ConcatcKeys, ItemsTableKeys, SupermarketTableKeys, ItemTables
from uuid import uuid1
import re


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
    db.dropTables()
    db.printTables()
    db.closeConnection()


def fetchData():
    api = Apis()
    api.fetchFoodStuffsItems(SuperMarketAbbreviation.newWorld)
    api.fetchFoodStuffsItems(SuperMarketAbbreviation.packNSave)
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
    countdowPage = 1
    newWorldPages = {}
    packNSavePages = {}

    countdowPageCount = 0
    newWorldPageCounts = {}
    packNSavePageCounts = {}

    values = []
    psItemsDict = {}
    nwItemsDict = {}
    cdItemsDict = {}

    # TODO: move page to items rather that ids
    for index, item in enumerate(sorted(items.values(), key=lambda x: sortingKey(x))):
        itemId = str(uuid1())
        itemValues = [itemId, item[ItemsTableKeys.category.value], item[ItemsTableKeys.brand.value]]
        if item[ConcatcKeys.countdownItemNames.value]:
            cdItemsDict[itemId] = {
                SupermarketTableKeys.itemId.value: itemId,
                SupermarketTableKeys.name.value: parseItemToString(item[ConcatcKeys.countdownItemNames.value]),
                SupermarketTableKeys.price.value: parseItemToString(item[ConcatcKeys.countdownPrices.value]),
                SupermarketTableKeys.size.value: parseItemToString(item[ConcatcKeys.countdownSizes.value]),
                SupermarketTableKeys.photoUrl.value: parseItemToString(item[ConcatcKeys.countdownphotoUrls.value]),
                SupermarketTableKeys.page.value: f'{countdowPage}'
            }
            countdowPageCount += 1

        for nwId in item[ConcatcKeys.newWorldItemNames.value].keys():
            name = parseItemToString(item[ConcatcKeys.newWorldItemNames.value][nwId])
            price = parseItemToString(item[ConcatcKeys.newWorldPrices.value][nwId])
            size = parseItemToString(item[ConcatcKeys.newWorldSizes.value][nwId])
            url = parseItemToString(item[ConcatcKeys.newWorldphotoUrls.value][nwId])
            if nwId not in newWorldPages:
                newWorldPages[nwId] = 1
            page = newWorldPages[nwId]
            nwItemsDict[itemId] = {
                SupermarketTableKeys.itemId.value: itemId,
                SupermarketTableKeys.name.value: name,
                SupermarketTableKeys.price.value: price,
                SupermarketTableKeys.size.value: size,
                SupermarketTableKeys.photoUrl.value: url,
                SupermarketTableKeys.supermarketId.value: nwId,
                SupermarketTableKeys.page.value: f'{page}'
            }
            if nwId not in newWorldPageCounts.keys():
                newWorldPageCounts[nwId] = 0
            newWorldPageCounts[nwId] = newWorldPageCounts[nwId] + 1

        for psId in item[ConcatcKeys.packNSaveItemNames.value].keys():
            name = parseItemToString(item[ConcatcKeys.packNSaveItemNames.value][psId])
            price = parseItemToString(item[ConcatcKeys.packNSavePrices.value][psId])
            size = parseItemToString(item[ConcatcKeys.packNSaveSizes.value][psId])
            url = parseItemToString(item[ConcatcKeys.packNSavephotoUrls.value][psId])
            if psId not in packNSavePages:
                packNSavePages[psId] = 1
            page = packNSavePages[psId]
            psItemsDict[itemId] = {
                SupermarketTableKeys.itemId.value: itemId,
                SupermarketTableKeys.name.value: name,
                SupermarketTableKeys.price.value: price,
                SupermarketTableKeys.size.value: size,
                SupermarketTableKeys.photoUrl.value: url,
                SupermarketTableKeys.supermarketId.value: psId,
                SupermarketTableKeys.page.value: f'{page}'
            }
            if psId not in packNSavePageCounts.keys():
                packNSavePageCounts[psId] = 0
            packNSavePageCounts[psId] = packNSavePageCounts[psId] + 1

        values.append(itemValues)

        if countdowPageCount > 0 and countdowPageCount % itemsPerPage == 0:
            countdowPageCount = 0
            countdowPage += 1

        for nwId in newWorldPageCounts.keys():
            if newWorldPageCounts[nwId] > 0 and newWorldPageCounts[nwId] % itemsPerPage == 0:
                newWorldPages[nwId] = newWorldPages[nwId] + 1
                newWorldPageCounts[nwId] = 0

        for psId in packNSavePageCounts.keys():
            if packNSavePageCounts[psId] > 0 and packNSavePageCounts[psId] % itemsPerPage == 0:
                packNSavePages[psId] = packNSavePages[psId] + 1
                packNSavePageCounts[psId] = 0

    cdValues = []
    nwValues = []
    psValues = []
    out = open("out.txt", mode="w")
    for item in values:
        itemId = item[0]
        if itemId in cdItemsDict.keys():
            cdItem = []
            cdDictItem = cdItemsDict[itemId]
            for key in SupermarketTableKeys:
                if key == SupermarketTableKeys.supermarketId:
                    continue
                cdItem.append(cdDictItem[key.value])
            cdValues.append(cdItem)

        if itemId in nwItemsDict.keys():
            nwItem = []
            nwDictItem = nwItemsDict[itemId]
            for key in SupermarketTableKeys:
                nwItem.append(nwDictItem[key.value])
            nwValues.append(nwItem)

        if itemId in psItemsDict.keys():
            psItem = []
            psDictItem = psItemsDict[itemId]
            for key in SupermarketTableKeys:
                psItem.append(psDictItem[key.value])
            psValues.append(psItem)

        if item[0] in cdItemsDict.keys() and item[0] in nwItemsDict.keys() and item[0] in psItemsDict.keys():
            out.write(str(cdItemsDict[item[0]]["name"]) + "\n")
            out.write(str(nwItemsDict[item[0]]["name"]) + "\n")
            out.write(str(psItemsDict[item[0]]["name"]) + "\n")
            out.write("-" * 100 + "\n")
    out.close()
    db.startConnection()

    db.insertItems(values, ItemTables.items)
    db.insertItems(cdValues, ItemTables.countdown)
    db.insertItems(psValues, ItemTables.pakNSave)
    db.insertItems(nwValues, ItemTables.newWorld)

    db.closeConnection()


def sortingKey(item) -> str:
    names = []
    for nameString in item[ConcatcKeys.countdownItemNames.value]:
        for name in nameString.split("@"):
            numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
            for number in numbers:
                name = name.replace(number, "")
            names.append(name)

    for nameKey in item[ConcatcKeys.packNSaveItemNames.value].keys():
        for nameString in item[ConcatcKeys.packNSaveItemNames.value][nameKey]:
            for name in nameString.split("@"):
                numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
                for number in numbers:
                    name = name.replace(number, "")
                names.append(name)
        break

    for nameKey in item[ConcatcKeys.newWorldItemNames.value].keys():
        for nameString in item[ConcatcKeys.newWorldItemNames.value][nameKey]:
            for name in nameString.split("@"):
                numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
                for number in numbers:
                    name = name.replace(number, "")
                names.append(name)
        break
    names = sorted(names)
    return names[0]


def parseItemToString(values) -> str:
    itemString = ''
    for value in values:
        itemString += f'{value.replace("[", "").replace("]", "")}@'

    return itemString[:-1]


def _populateItem(items, dictionary, itemName, itemExists, brand, supermarket: SupportedStores):
    if not itemExists:
        items[itemName] = {}
        items[itemName][ConcatcKeys.newWorldItemNames.value] = {}
        items[itemName][ConcatcKeys.newWorldPrices.value] = {}
        items[itemName][ConcatcKeys.newWorldSizes.value] = {}
        items[itemName][ConcatcKeys.newWorldphotoUrls.value] = {}

        items[itemName][ConcatcKeys.countdownItemNames.value] = []
        items[itemName][ConcatcKeys.countdownPrices.value] = []
        items[itemName][ConcatcKeys.countdownSizes.value] = []
        items[itemName][ConcatcKeys.countdownphotoUrls.value] = []

        items[itemName][ConcatcKeys.packNSaveSizes.value] = {}
        items[itemName][ConcatcKeys.packNSaveItemNames.value] = {}
        items[itemName][ConcatcKeys.packNSavePrices.value] = {}
        items[itemName][ConcatcKeys.packNSavephotoUrls.value] = {}

        items[itemName][ConcatcKeys.category.value] = dictionary[OutputJsonKeys.category.value]
        items[itemName][ConcatcKeys.brand.value] = brand

    names = items[itemName][ConcatcKeys.countdownItemNames.value]
    prices = items[itemName][ConcatcKeys.countdownPrices.value]
    sizes = items[itemName][ConcatcKeys.countdownSizes.value]
    urls = items[itemName][ConcatcKeys.countdownphotoUrls.value]
    if supermarket == SupportedStores.newWorld:
        names = items[itemName][ConcatcKeys.newWorldItemNames.value]
        sizes = items[itemName][ConcatcKeys.newWorldSizes.value]
        for key in names.keys():
            for index in range(0, len(names[key])):
                if names[key][index] == dictionary[OutputJsonKeys.name.value] and \
                        dictionary["size"] == sizes[key][index]:
                    return

        prices = items[itemName][ConcatcKeys.newWorldPrices.value]
        urls = items[itemName][ConcatcKeys.newWorldphotoUrls.value]

    elif supermarket == SupportedStores.packNSave:
        names = items[itemName][ConcatcKeys.packNSaveItemNames.value]
        sizes = items[itemName][ConcatcKeys.packNSaveSizes.value]
        for key in names.keys():
            for index in range(0, len(names[key])):
                if names[key][index] == dictionary[OutputJsonKeys.name.value] and \
                        dictionary["size"] == sizes[key][index]:
                    return

        prices = items[itemName][ConcatcKeys.packNSavePrices.value]
        urls = items[itemName][ConcatcKeys.packNSavephotoUrls.value]

    else:
        for index, item in enumerate(names):
            if item == dictionary[OutputJsonKeys.name.value] and dictionary["size"] == sizes[index]:
                return

        names.append(dictionary[OutputJsonKeys.name.value])
        prices.append(dictionary[OutputJsonKeys.price.value])
        sizes.append(dictionary["size"])
        urls.append(dictionary["photoUrl"])

    if supermarket == SupportedStores.newWorld or supermarket == SupportedStores.packNSave:
        for priceKey in dictionary[OutputJsonKeys.price.value].keys():
            if priceKey in prices.keys():
                prices[priceKey].append(dictionary[OutputJsonKeys.price.value][priceKey])
                names[priceKey].append(dictionary[OutputJsonKeys.name.value])
                sizes[priceKey].append(dictionary[OutputJsonKeys.size.value])
                urls[priceKey].append(dictionary[OutputJsonKeys.photoUrl.value])
            else:
                prices[priceKey] = [dictionary[OutputJsonKeys.price.value][priceKey]]
                names[priceKey] = [dictionary[OutputJsonKeys.name.value]]
                sizes[priceKey] = [dictionary[OutputJsonKeys.size.value]]
                urls[priceKey] = [dictionary[OutputJsonKeys.photoUrl.value]]

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
    # json.dump(items, f)
    # f.close()

    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()


dropTables()
createTables()
clusterData()
# fetchData()
# Apis().fetchCountdownItems()
