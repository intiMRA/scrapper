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
    numberOfStoresFile = open("numberOfStoresFile.txt", mode="w")
    api.fetchFoodStuffsItems(SuperMarketAbbreviation.newWorld, numberOfStoresFile)
    api.fetchFoodStuffsItems(SuperMarketAbbreviation.packNSave, numberOfStoresFile)
    numberOfStoresFile.close()
    api.fetchCountdownItems()


def concatCategory(oldCategory: str, newCategoryString: str) -> str:
    newCategories = newCategoryString.split("@")
    for newCategory in newCategories:
        if newCategory not in oldCategory:
            oldCategory += '@' + newCategory
    return oldCategory


def writeItemsToDB(items):
    db = Database()
    maxItemsPerQuery = 1000
    itemsPerPage = 50
    countdowPage = 1
    newWorldPages = {}
    packNSavePages = {}

    countdowPageCount = 0
    newWorldPageCounts = {}
    packNSavePageCounts = {}

    itemValues = []
    psItemsDict = {}
    nwItemsDict = {}
    cdItemsDict = {}
    numberOfStoresFile = open("numberOfStoresFile.txt", mode="r")
    numberOfStoresFileRead = numberOfStoresFile.read()
    numberOfNewWorldStores = int(numberOfStoresFileRead[0])
    numberOfPackNSaveStores = int(numberOfStoresFileRead[1])
    numberOfStoresFile.close()
    for index, item in enumerate(sorted(items.values(), key=lambda x: sortingKey(x, numberOfNewWorldStores, numberOfPackNSaveStores))):
        itemId = str(uuid1())
        itemValue = [itemId, item[ItemsTableKeys.category.value], item[ItemsTableKeys.brand.value]]
        itemValues.append(itemValue)
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
        # TODO: item id is overriding, we need a list of newworld supermarket
        for nwId in item[ConcatcKeys.newWorldItemNames.value].keys():
            name = parseItemToString(item[ConcatcKeys.newWorldItemNames.value][nwId])
            price = parseItemToString(item[ConcatcKeys.newWorldPrices.value][nwId])
            size = parseItemToString(item[ConcatcKeys.newWorldSizes.value][nwId])
            url = parseItemToString(item[ConcatcKeys.newWorldphotoUrls.value][nwId])
            if nwId not in newWorldPages:
                newWorldPages[nwId] = 1
            page = newWorldPages[nwId]
            if nwId not in nwItemsDict.keys():
                nwItemsDict[nwId] = {}
            nwItemsDict[nwId][itemId] = {
                SupermarketTableKeys.itemId.value: itemId,
                SupermarketTableKeys.name.value: name,
                SupermarketTableKeys.price.value: price,
                SupermarketTableKeys.size.value: size,
                SupermarketTableKeys.photoUrl.value: url,
                SupermarketTableKeys.page.value: f'{page}',
                SupermarketTableKeys.supermarketId.value: nwId
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
            if psId not in psItemsDict.keys():
                psItemsDict[psId] = {}
            psItemsDict[psId][itemId] = {
                SupermarketTableKeys.itemId.value: itemId,
                SupermarketTableKeys.name.value: name,
                SupermarketTableKeys.price.value: price,
                SupermarketTableKeys.size.value: size,
                SupermarketTableKeys.photoUrl.value: url,
                SupermarketTableKeys.page.value: f'{page}',
                SupermarketTableKeys.supermarketId.value: psId
            }
            if psId not in packNSavePageCounts.keys():
                packNSavePageCounts[psId] = 0
            packNSavePageCounts[psId] = packNSavePageCounts[psId] + 1

        if countdowPageCount >= itemsPerPage:
            countdowPageCount = 0
            countdowPage += 1
        newCounts = {}
        for nwId in newWorldPageCounts.keys():
            if newWorldPageCounts[nwId] >= itemsPerPage:
                newWorldPages[nwId] = newWorldPages[nwId] + 1
                newCounts[nwId] = 0
            else:
                newCounts[nwId] = newWorldPageCounts[nwId]
        newWorldPageCounts = newCounts
        newCounts = {}
        for psId in packNSavePageCounts.keys():
            if packNSavePageCounts[psId] >= itemsPerPage:
                packNSavePages[psId] = packNSavePages[psId] + 1
                newCounts[psId] = 0
            else:
                newCounts[psId] = packNSavePageCounts[psId]
        packNSavePageCounts = newCounts
    countdownValues = []
    newWorldValues = []
    packNSaveValues = []
    for item in itemValues:
        itemId = item[0]
        if itemId in cdItemsDict.keys():
            cdItem = []
            cdDictItem = cdItemsDict[itemId]
            for key in SupermarketTableKeys:
                if key == SupermarketTableKeys.supermarketId:
                    continue
                cdItem.append(cdDictItem[key.value])
            countdownValues.append(cdItem)
        for store in nwItemsDict.values():
            if itemId in store.keys():
                nwItem = []
                nwDictItem = store[itemId]
                for key in SupermarketTableKeys:
                    nwItem.append(nwDictItem[key.value])
                newWorldValues.append(nwItem)
        for store in psItemsDict.values():
            if itemId in store.keys():
                psItem = []
                psDictItem = store[itemId]
                for key in SupermarketTableKeys:
                    psItem.append(psDictItem[key.value])
                packNSaveValues.append(psItem)
    db.startConnection()
    packNSaveQueryNumber = len(packNSaveValues) // maxItemsPerQuery
    newWorldQueryNumber = len(newWorldValues) // maxItemsPerQuery
    countdownQueryNumber = len(countdownValues) // maxItemsPerQuery
    itemsQueryNumber = len(itemValues) // maxItemsPerQuery
    for i in range(0, itemsQueryNumber):
        if (i + 1) * 1000 >= len(itemValues):
            db.insertItems(itemValues[i*1000:-1], ItemTables.items)
        else:
            db.insertItems(itemValues[i * 1000:(i+1)*1000], ItemTables.items)

    for i in range(0, countdownQueryNumber):
        if (i + 1) * 1000 >= len(countdownValues):
            db.insertItems(countdownValues[i*1000:-1], ItemTables.countdown)
        else:
            db.insertItems(countdownValues[i * 1000:(i+1)*1000], ItemTables.countdown)

    for i in range(0, packNSaveQueryNumber):
        if (i + 1) * 1000 >= len(packNSaveValues):
            db.insertItems(packNSaveValues[i*1000:-1], ItemTables.pakNSave)
        else:
            db.insertItems(packNSaveValues[i * 1000:(i+1)*1000], ItemTables.pakNSave)

    for i in range(0, newWorldQueryNumber):
        if (i + 1) * 1000 >= len(newWorldValues):
            db.insertItems(newWorldValues[i*1000:-1], ItemTables.newWorld)
        else:
            db.insertItems(newWorldValues[i * 1000:(i+1)*1000], ItemTables.newWorld)

    db.closeConnection()


def sortingKey(item, numberOfNewWorldStores, numberOfPackNSaveStores) -> tuple:
    names = []
    count = 0.0
    if len(item[ConcatcKeys.countdownItemNames.value]) > 0:
        count = -1

    for nameString in item[ConcatcKeys.countdownItemNames.value]:
        for name in nameString.split("@"):
            name = name.replace("&", "").replace("@", "")
            numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
            for number in numbers:
                name = name.replace(number, "")
            names.append(name)

    lenPS = len(item[ConcatcKeys.packNSaveItemNames.value].keys())
    count -= ((1 / numberOfPackNSaveStores) * lenPS)
    for nameKey in item[ConcatcKeys.packNSaveItemNames.value].keys():
        for nameString in item[ConcatcKeys.packNSaveItemNames.value][nameKey]:
            for name in nameString.split("@"):
                name = name.replace("&", "").replace("@", "")
                numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
                for number in numbers:
                    name = name.replace(number, "")
                names.append(name)
        break

    lenNW = len(item[ConcatcKeys.newWorldItemNames.value].keys())
    count -= ((1 / numberOfNewWorldStores) * lenNW)
    for nameKey in item[ConcatcKeys.newWorldItemNames.value].keys():
        for nameString in item[ConcatcKeys.newWorldItemNames.value][nameKey]:
            for name in nameString.split("@"):
                name = name.replace("&", "").replace("@", "")
                numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
                for number in numbers:
                    name = name.replace(number, "")
                names.append(name)
        break
    names = sorted(names)
    if count > -1:
        count = -1
    return (count, names[0])


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

    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()

dropTables()
createTables()
# fetchData()
clusterData()
# fetchData()
# Apis().fetchCountdownItems()
