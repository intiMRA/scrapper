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
    with open("numberOfStoresFile.txt", mode="w") as numberOfStoresFile:
        numberOfStores = [api.fetchFoodStuffsItems(key) for key in SuperMarketAbbreviation]
        numberOfStoresFile.write(','.join(numberOfStores))
        api.fetchCountdownItems()


def concatCategory(oldCategory: str, newCategoryString: str) -> str:
    newCategories = newCategoryString.split("@")
    for newCategory in newCategories:
        if newCategory not in oldCategory:
            oldCategory += '@' + newCategory
    return oldCategory


def writeItemsToDB(items: dict[str, any]):
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
    with open("numberOfStoresFile.txt", mode="r") as f:
        numberOfNewWorldStores, numberOfPackNSaveStores = map(int, f.read().split(','))
    items = sorted(items.values(), key=lambda x: sortingKey(x, numberOfNewWorldStores, numberOfPackNSaveStores))
    for index, item in enumerate(items):
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

    countdownValues = [
        [cdDictItem[key.value] for key in SupermarketTableKeys if key != SupermarketTableKeys.supermarketId] for
        itemId, cdDictItem in cdItemsDict.items() if itemId in [item[0] for item in itemValues]]

    newWorldValues = [[nwDictItem[key.value] for key in SupermarketTableKeys] for store in nwItemsDict.values() for
                      itemId, nwDictItem in store.items() if itemId in [item[0] for item in itemValues]]

    packNSaveValues = [[psDictItem[key.value] for key in SupermarketTableKeys] for store in psItemsDict.values() for
                       itemId, psDictItem in store.items() if itemId in [item[0] for item in itemValues]]

    # countdownValues = []
    # newWorldValues = []
    # packNSaveValues = []
    # for item in itemValues:
    #     itemId = item[0]
    #     if itemId in cdItemsDict.keys():
    #         cdItem = []
    #         cdDictItem = cdItemsDict[itemId]
    #         for key in SupermarketTableKeys:
    #             if key == SupermarketTableKeys.supermarketId:
    #                 continue
    #             cdItem.append(cdDictItem[key.value])
    #         countdownValues.append(cdItem)
    #     for store in nwItemsDict.values():
    #         if itemId in store.keys():
    #             nwItem = []
    #             nwDictItem = store[itemId]
    #             for key in SupermarketTableKeys:
    #                 nwItem.append(nwDictItem[key.value])
    #             newWorldValues.append(nwItem)
    #     for store in psItemsDict.values():
    #         if itemId in store.keys():
    #             psItem = []
    #             psDictItem = store[itemId]
    #             for key in SupermarketTableKeys:
    #                 psItem.append(psDictItem[key.value])
    #             packNSaveValues.append(psItem)
    db.startConnection()
    # Insert items into the main items table
    for i in range(0, len(itemValues), maxItemsPerQuery):
        db.insertItems(itemValues[i:i + maxItemsPerQuery], ItemTables.items)

    # Insert values into the three supermarket-specific tables
    tables = {
        ItemTables.countdown: countdownValues,
        ItemTables.pakNSave: packNSaveValues,
        ItemTables.newWorld: newWorldValues,
    }
    for table, values in tables.items():
        for i in range(0, len(values), maxItemsPerQuery):
            db.insertItems(values[i:i + maxItemsPerQuery], table)

    db.closeConnection()


def sortingKey(item: dict[str, any], numberOfNewWorldStores: int, numberOfPackNSaveStores: int) -> tuple:
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
    return count, names[0]


def parseItemToString(values: list[str]) -> str:
    itemString = ''
    for value in values:
        itemString += f'{value.replace("[", "").replace("]", "")}@'

    return itemString[:-1]


def _populateItem(items: dict[str, any],
                  dictionary: dict[str, any],
                  itemName: str,
                  itemExists: bool,
                  brand: str,
                  supermarket: SupportedStores):
    if not itemExists:
        items[itemName] = {}

        for key in [ConcatcKeys.countdownItemNames.value,
                    ConcatcKeys.countdownPrices.value,
                    ConcatcKeys.countdownSizes.value,
                    ConcatcKeys.countdownphotoUrls.value]:
            items[itemName][key] = []

        for key in [ConcatcKeys.packNSaveSizes.value,
                    ConcatcKeys.packNSaveItemNames.value,
                    ConcatcKeys.packNSavePrices.value,
                    ConcatcKeys.packNSavephotoUrls.value,
                    ConcatcKeys.newWorldItemNames.value,
                    ConcatcKeys.newWorldPrices.value,
                    ConcatcKeys.newWorldSizes.value,
                    ConcatcKeys.newWorldphotoUrls.value]:
            items[itemName][key] = {}

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
    stopSet = read_json_file("stopWords.json")["nonKeyWords"]

    countdownDict = read_json_file("countDownData.json")
    newWorldDict = read_json_file("newWorldData.json")
    packNSaveDict = read_json_file("packNSaveData.json")

    newWorldKeyMap = {finalCategories.transformToKey(key): key for key in newWorldDict.keys()}
    packNSaveKeyMap = {finalCategories.transformToKey(key): key for key in packNSaveDict.keys()}
    countdownKeyMap = {finalCategories.transformToKey(key): key for key in countdownDict.keys()}
    newWorldKeys = [finalCategories.transformToKey(key) for key in newWorldDict.keys()]
    packNSaveKeys = [finalCategories.transformToKey(key) for key in packNSaveDict.keys()]
    countdownKeys = [finalCategories.transformToKey(key) for key in countdownDict.keys()]

    items = {}
    for key in countdownDict.keys():
        brand = countdownDict[key]
        ckm = finalCategories.transformToKey(key)
        countdownKeys.remove(ckm)
        for countDownItem in brand:
            countdownName = finalCategories.transformItem(countDownItem[OutputJsonKeys.name.value], stopSet)

            _populateItem(items,
                          countDownItem,
                          countdownName,
                          countdownName in items.keys(),
                          key,
                          SupportedStores.countdown)

            if ckm in newWorldKeyMap:
                for newWorldItem in newWorldDict[newWorldKeyMap[ckm]]:
                    newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)

                    itemExists = fuzz.partial_ratio(newWorldName, countdownName) > treshold and \
                                 (countdownName in items.keys() or
                                  newWorldName in items.keys())
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
                                 (countdownName in items.keys() or
                                  pakNSaveName in items.keys())
                    name = pakNSaveName
                    if itemExists:
                        name = countdownName
                    _populateItem(items, packNSaveItem, name, itemExists, key, SupportedStores.packNSave)
            if ckm in packNSaveKeys:
                packNSaveKeys.remove(ckm)

    commonKeys = set(newWorldKeyMap.keys()) & set(packNSaveKeyMap.keys())
    for key in commonKeys:
        for newWorldItem in newWorldDict[newWorldKeyMap[key]]:
            newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)

            _populateItem(items, newWorldItem, newWorldName, newWorldName in items.keys(), newWorldKeyMap[key],
                          SupportedStores.newWorld)

            for packNSaveItem in packNSaveDict[packNSaveKeyMap[key]]:
                pakNSaveName = finalCategories.transformItem(packNSaveItem[OutputJsonKeys.name.value], stopSet)

                itemExists = fuzz.partial_ratio(pakNSaveName, newWorldName) > treshold and \
                             (pakNSaveName in items.keys() or
                              newWorldName in items.keys())
                name = pakNSaveName
                if itemExists:
                    name = newWorldName
                _populateItem(items, packNSaveItem, name, itemExists, newWorldKeyMap[key],
                              SupportedStores.packNSave)
        if key in packNSaveKeys:
            packNSaveKeys.remove(key)
        if key in newWorldKeys:
            newWorldKeys.remove(key)

    packNSaveKeys = [key for key in packNSaveKeys if key not in commonKeys]
    newWorldKeys = [key for key in newWorldKeys if key not in commonKeys]

    for ck in countdownKeys:
        for countDownItem in countdownDict[countdownKeyMap[ck]]:
            countdownName = finalCategories.transformItem(countDownItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, countDownItem, countdownName, countdownName in items.keys(), countdownKeyMap[ck],
                          SupportedStores.countdown)

    for nwk in newWorldKeys:
        for newWorldItem in newWorldDict[newWorldKeyMap[nwk]]:
            newWorldName = finalCategories.transformItem(newWorldItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, newWorldItem, newWorldName, newWorldName in items.keys(), newWorldKeyMap[nwk],
                          SupportedStores.newWorld)

    for psk in packNSaveKeys:
        for pakNSaveItem in packNSaveDict[packNSaveKeyMap[psk]]:
            pakNSaveName = finalCategories.transformItem(pakNSaveItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items, pakNSaveItem, pakNSaveName, pakNSaveName in items.keys(), packNSaveKeyMap[psk],
                          SupportedStores.packNSave)
    writeItemsToDB(items)


def read_json_file(file_name) -> dict[str, any]:
    with open(file_name) as file:
        data = json.load(file)
    return data


dropTables()
createTables()
# fetchData()
clusterData()
# fetchData()
# Apis().fetchCountdownItems()
