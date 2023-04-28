import json
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories
from SuperMarketsApis import OutputJsonKeys
from fuzzywuzzy.fuzz import token_sort_ratio as ratio
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
    print("start decluster")
    db = Database()
    maxItemsPerQuery = 1000
    itemsPerPage = 50
    countdownPage = 1
    newWorldPages = {}
    packNSavePages = {}

    countdownPageCount = 0
    newWorldPageCounts = {}
    packNSavePageCounts = {}

    itemValues = []
    psItemsDict = {}
    nwItemsDict = {}
    cdItemsDict = {}
    with open("numberOfStoresFile.txt", mode="r") as f:
        numberOfNewWorldStores, numberOfPackNSaveStores = map(int, f.read().split(','))
    items = sorted(items.values(), key=lambda x: sortingKey(x, numberOfNewWorldStores, numberOfPackNSaveStores))
    print("all sorted")
    for item in items:
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
                SupermarketTableKeys.page.value: f'{countdownPage}'
            }
            countdownPageCount += 1

        nwCounts = {}
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
                newWorldPageCounts[nwId] = 1
            else:
                newWorldPageCounts[nwId] = newWorldPageCounts[nwId] + 1

            if newWorldPageCounts[nwId] >= itemsPerPage:
                newWorldPages[nwId] = newWorldPages[nwId] + 1
                nwCounts[nwId] = 0
            else:
                nwCounts[nwId] = newWorldPageCounts[nwId]
        newWorldPageCounts = nwCounts

        psCounts = {}
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
                packNSavePageCounts[psId] = 1
            else:
                packNSavePageCounts[psId] = packNSavePageCounts[psId] + 1

            if packNSavePageCounts[psId] >= itemsPerPage:
                packNSavePages[psId] = packNSavePages[psId] + 1
                psCounts[psId] = 0
            else:
                psCounts[psId] = packNSavePageCounts[psId]
        packNSavePageCounts = psCounts

        if countdownPageCount >= itemsPerPage:
            countdownPageCount = 0
            countdownPage += 1

    countdownValues = [
        [cdDictItem[key.value] for key in SupermarketTableKeys if key != SupermarketTableKeys.supermarketId] for
        itemId, cdDictItem in cdItemsDict.items() if itemId in [item[0] for item in itemValues]]

    newWorldValues = [[nwDictItem[key.value] for key in SupermarketTableKeys] for store in nwItemsDict.values() for
                      itemId, nwDictItem in store.items() if itemId in [item[0] for item in itemValues]]

    packNSaveValues = [[psDictItem[key.value] for key in SupermarketTableKeys] for store in psItemsDict.values() for
                       itemId, psDictItem in store.items() if itemId in [item[0] for item in itemValues]]

    db.startConnection()
    allQueries = (len(itemValues) // maxItemsPerQuery) \
                 + (len(countdownValues) // maxItemsPerQuery) \
                 + (len(packNSaveValues) // maxItemsPerQuery) \
                 + (len(newWorldValues) // maxItemsPerQuery)
    queryCount = 0
    # Insert items into the main items table
    for i in range(0, len(itemValues), maxItemsPerQuery):
        db.insertItems(itemValues[i:i + maxItemsPerQuery], ItemTables.items)
        queryCount += 1
        percentage = queryCount / allQueries
        print(f"{percentage:.2%} of queries done")
    # Insert values into the three supermarket-specific tables
    tables = {
        ItemTables.countdown: countdownValues,
        ItemTables.pakNSave: packNSaveValues,
        ItemTables.newWorld: newWorldValues,
    }
    for table, values in tables.items():
        for i in range(0, len(values), maxItemsPerQuery):
            db.insertItems(values[i:i + maxItemsPerQuery], table)
            queryCount += 1
            percentage = queryCount / allQueries
            print(f"{percentage:.2%} of queries done")

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
    itemName = itemName + brand
    if (not itemExists) and itemName not in items.keys():
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
                        dictionary[OutputJsonKeys.size.value] == sizes[key][index]:
                    return

        prices = items[itemName][ConcatcKeys.newWorldPrices.value]
        urls = items[itemName][ConcatcKeys.newWorldphotoUrls.value]

    elif supermarket == SupportedStores.packNSave:
        names = items[itemName][ConcatcKeys.packNSaveItemNames.value]
        sizes = items[itemName][ConcatcKeys.packNSaveSizes.value]
        for key in names.keys():
            for index in range(0, len(names[key])):
                if names[key][index] == dictionary[OutputJsonKeys.name.value] and \
                        dictionary[OutputJsonKeys.size.value] == sizes[key][index]:
                    return

        prices = items[itemName][ConcatcKeys.packNSavePrices.value]
        urls = items[itemName][ConcatcKeys.packNSavephotoUrls.value]

    else:
        for index, item in enumerate(names):
            if item == dictionary[OutputJsonKeys.name.value] and dictionary[OutputJsonKeys.size.value] == sizes[index]:
                return

        names.append(dictionary[OutputJsonKeys.name.value])
        prices.append(dictionary[OutputJsonKeys.price.value])
        sizes.append(dictionary[OutputJsonKeys.size.value])
        urls.append(dictionary[OutputJsonKeys.photoUrl.value])

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
    treshold = 85
    stopSet = read_json_file("stopWords.json")["nonKeyWords"]

    countdownDict = read_json_file("countDownData.json")
    newWorldDict = read_json_file("newWorldData.json")
    packNSaveDict = read_json_file("packNSaveData.json")

    newWorldKeyMap = {finalCategories.transformToKey(key): key for key in newWorldDict.keys()}
    packNSaveKeyMap = {finalCategories.transformToKey(key): key for key in packNSaveDict.keys()}
    countdownKeyMap = {finalCategories.transformToKey(key): key for key in countdownDict.keys()}
    newWorldKeys = set([finalCategories.transformToKey(key) for key in newWorldDict.keys()])
    packNSaveKeys = set([finalCategories.transformToKey(key) for key in packNSaveDict.keys()])
    countdownKeys = set([finalCategories.transformToKey(key) for key in countdownDict.keys()])

    allCommonKeys = newWorldKeys & countdownKeys & packNSaveKeys

    packNSaveCountDownKeys = (packNSaveKeys & countdownKeys) - allCommonKeys
    newWorldCountDownKeys = (newWorldKeys & countdownKeys) - allCommonKeys
    packNSaveNewworldKeys = (packNSaveKeys & newWorldKeys) - allCommonKeys

    overlappingKeys = allCommonKeys & newWorldCountDownKeys & packNSaveCountDownKeys & packNSaveNewworldKeys
    countdownKeys -= overlappingKeys
    packNSaveKeys -= overlappingKeys
    newWorldKeys -= overlappingKeys

    items = {}
    for allCommonKey in allCommonKeys:
        packNSaveMappedKey = packNSaveKeyMap[allCommonKey]
        newWorldMappedKey = newWorldKeyMap[allCommonKey]
        countdownMappedKey = countdownKeyMap[allCommonKey]

        packNSaveItems = packNSaveDict[packNSaveMappedKey]
        newWorldItems = newWorldDict[newWorldMappedKey]
        countdownItems = countdownDict[countdownMappedKey]

        for countdownItem in countdownItems:
            countdownName = finalCategories.transformItem(countdownItem[OutputJsonKeys.name.value], stopSet)
            _populateItem(items,
                          countdownItem,
                          countdownName,
                          countdownName in items.keys(),
                          countdownMappedKey,
                          SupportedStores.countdown)

            itemTuples = [(newWorldItems, SupportedStores.newWorld), (packNSaveItems, SupportedStores.packNSave)]
            for itemTuple in itemTuples:
                itemsList, supportedStore = itemTuple
                for otherItem in itemsList:
                    otherItemName = finalCategories.transformItem(otherItem[OutputJsonKeys.name.value], stopSet)
                    itemExists = getRatio(otherItemName, countdownName) > treshold
                    name = otherItemName
                    if itemExists:
                        name = countdownName
                    _populateItem(items, otherItem, name, itemExists, countdownMappedKey, supportedStore)

    pairs = [(newWorldCountDownKeys,
              (countdownDict, SupportedStores.countdown, countdownKeyMap),
              (newWorldDict, SupportedStores.newWorld, newWorldKeyMap)),

             (packNSaveCountDownKeys,
              (countdownDict, SupportedStores.countdown, countdownKeyMap),
              (packNSaveDict, SupportedStores.packNSave, packNSaveKeyMap)),

             (packNSaveNewworldKeys,
              (packNSaveDict, SupportedStores.packNSave, packNSaveKeyMap),
              (newWorldDict, SupportedStores.newWorld, newWorldKeyMap))]

    for pair in pairs:
        keys, supermarket1Tuple, supermarket2Tuple = pair
        for key in keys:
            supermarket1Dict, supermarket1Name, supermarket1KeyMap = supermarket1Tuple
            supermarket2Dict, supermarket2Name, supermarket2KeyMap = supermarket2Tuple
            supermarket1Key = supermarket1KeyMap[key]
            supermarket2Key = supermarket2KeyMap[key]

            for supermarket1Item in supermarket1Dict[supermarket1Key]:
                supermarket1ItemName = finalCategories.transformItem(supermarket1Item[OutputJsonKeys.name.value],
                                                                     stopSet)
                _populateItem(items,
                              supermarket1Item,
                              supermarket1ItemName,
                              supermarket1ItemName in items.keys(),
                              supermarket1Key,
                              supermarket1Name)

                for supermarket2Item in supermarket2Dict[supermarket2Key]:
                    supermarket2ItemName = finalCategories.transformItem(supermarket2Item[OutputJsonKeys.name.value],
                                                                         stopSet)
                    itemExists = getRatio(supermarket2ItemName, supermarket1ItemName) > treshold
                    name = supermarket2ItemName
                    if itemExists:
                        name = supermarket1ItemName

                    _populateItem(items,
                                  supermarket2Item,
                                  name,
                                  itemExists,
                                  supermarket1Key,
                                  supermarket2Name)

    supermarketTuples = [(countdownKeys, countdownDict, SupportedStores.countdown, countdownKeyMap),
                         (newWorldKeys, newWorldDict, SupportedStores.newWorld, newWorldKeyMap),
                         (packNSaveKeys, packNSaveDict, SupportedStores.packNSave, packNSaveKeyMap)]

    for supermarketTuple in supermarketTuples:
        supermarketKeys, supermarketDict, supermarketName, supermarketKeyMap = supermarketTuple
        for key in supermarketKeys:
            mappedKey = supermarketKeyMap[key]
            for superMarketItem in supermarketDict[mappedKey]:
                superMarketName = finalCategories.transformItem(superMarketItem[OutputJsonKeys.name.value], stopSet)

                _populateItem(items,
                              superMarketItem,
                              superMarketName,
                              superMarketName in items.keys(),
                              mappedKey,
                              supermarketName)

    print("cluster done")
    writeItemsToDB(items)


ratioCache = {}


def getRatio(name1, name2):
    key = (name1, name2)
    if key not in ratioCache:
        ratioCache[key] = ratio(name1, name2)
    return ratioCache[key]


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
