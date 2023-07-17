import json
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from SuperMarketsApis import SuperMarketAbbreviation
import finalCategories
from SuperMarketsApis import OutputJsonKeys
from fuzzywuzzy.fuzz import token_sort_ratio as ratio
from Database import ConcatcKeys, ItemsTableKeys, ItemTables
from uuid import uuid1
import re

debug = True


class SupportedStores(Enum):
    newWorld = "NewWorld"
    packNSave = "packNSave"
    countdown = "Countdown"


def createTables():
    db = Database(debug)
    db.startConnection()
    db.createTable()
    db.printTables()
    db.closeConnection()


def dropTables():
    db = Database(debug)
    db.startConnection()
    db.dropTables()
    db.printTables()
    db.closeConnection()


def fetchData():
    api = Apis()
    with open("numberOfStoresFile.txt", mode="w") as numberOfStoresFile:
        numberOfStores = [str(api.fetchFoodStuffsItems(key)) for key in SuperMarketAbbreviation]
        numberOfStoresFile.write(','.join(numberOfStores))
        api.fetchCountdownItems()


def concatCategory(oldCategory: str, newCategoryString: str) -> str:
    newCategories = newCategoryString.split("@")
    for newCategory in newCategories:
        if newCategory not in oldCategory:
            oldCategory += '@' + newCategory
    return oldCategory


def writeItemsToDB(items: dict[str, dict[str, any]]):
    print("start de-cluster")
    db = Database(debug)
    maxItemsPerQuery = 1000
    itemsPerPage = 50
    countdownPage = 1
    newWorldPages = {}
    packNSavePages = {}

    countdownPageCount = 0
    newWorldPageCounts = {}
    packNSavePageCounts = {}
    categories = []

    itemValues = []

    with open("numberOfStoresFile.txt", mode="r") as f:
        numberOfNewWorldStores, numberOfPackNSaveStores = map(int, f.read().split(','))
    items = sorted(items.values(), key=lambda x: sortingKey(x, numberOfNewWorldStores, numberOfPackNSaveStores))
    totalItems = len(items)
    print("all sorted")
    itemsCount = 0
    countdownValues = []
    newWorldValues = []
    packNSaveValues = []

    for item in items:
        itemId = str(uuid1())
        itemValue = [itemId, item[ItemsTableKeys.category.value], item[ItemsTableKeys.brand.value]]
        itemCategories = item[ItemsTableKeys.category.value]
        for cat in itemCategories.split("@"):
            if cat not in categories:
                categories.append(cat)
        itemValues.append(itemValue)
        if item[ConcatcKeys.countdownItemNames.value]:
            countdownItem = [itemId,
                             parseItemToString(item[ConcatcKeys.countdownItemNames.value]),
                             parseItemToString(item[ConcatcKeys.countdownPrices.value]),
                             parseItemToString(item[ConcatcKeys.countdownSizes.value]),
                             parseItemToString(item[ConcatcKeys.countdownphotoUrls.value]),
                             f'{countdownPage}']
            countdownValues.append(countdownItem)
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

            newWorldItem = [itemId,
                            name,
                            price,
                            size,
                            url,
                            f'{page}',
                            nwId]
            newWorldValues.append(newWorldItem)

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

            packNSaveItem = [itemId,
                             name,
                             price,
                             size,
                             url,
                             f'{page}',
                             psId]
            packNSaveValues.append(packNSaveItem)

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

        itemsCount += 1
        print(f"{itemsCount / totalItems:.2%} of items done")

    db.startConnection()
    db.insertCategoryNames(categories)
    allQueries = (len(itemValues) // maxItemsPerQuery) + \
                 (len(countdownValues) // maxItemsPerQuery) + \
                 (len(packNSaveValues) // maxItemsPerQuery) + \
                 (len(newWorldValues) // maxItemsPerQuery) + 4

    print(f'number of queries: {allQueries}')
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
            numbers = re.findall(r'[0-9]+[aA-zZ]? +', name)
            for number in numbers:
                name = name.replace(number, "")
            names.append(name)

    lenPS = len(item[ConcatcKeys.packNSaveItemNames.value].keys())
    count -= ((1 / numberOfPackNSaveStores) * lenPS)
    for nameKey in item[ConcatcKeys.packNSaveItemNames.value].keys():
        for nameString in item[ConcatcKeys.packNSaveItemNames.value][nameKey]:
            for name in nameString.split("@"):
                name = name.replace("&", "").replace("@", "")
                numbers = re.findall(r'[0-9]+[aA-zZ]? +', name)
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
                numbers = re.findall(r'[0-9]+[aA-zZ]? +', name)
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


brands = set()


def _populateItem(items: dict[str, any],
                  dictionary: dict[str, any],
                  itemId: str,
                  brand: str,
                  supermarket: SupportedStores):
    itemId = itemId.lower()
    if itemId not in items.keys():
        items[itemId] = {}
        for key in [ConcatcKeys.countdownItemNames.value,
                    ConcatcKeys.countdownPrices.value,
                    ConcatcKeys.countdownSizes.value,
                    ConcatcKeys.countdownphotoUrls.value]:
            items[itemId][key] = []

        for key in [ConcatcKeys.packNSaveSizes.value,
                    ConcatcKeys.packNSaveItemNames.value,
                    ConcatcKeys.packNSavePrices.value,
                    ConcatcKeys.packNSavephotoUrls.value,
                    ConcatcKeys.newWorldItemNames.value,
                    ConcatcKeys.newWorldPrices.value,
                    ConcatcKeys.newWorldSizes.value,
                    ConcatcKeys.newWorldphotoUrls.value]:
            items[itemId][key] = {}

        items[itemId][ConcatcKeys.category.value] = dictionary[OutputJsonKeys.category.value]
        items[itemId][ConcatcKeys.brand.value] = brand

    names = items[itemId][ConcatcKeys.countdownItemNames.value]
    prices = items[itemId][ConcatcKeys.countdownPrices.value]
    sizes = items[itemId][ConcatcKeys.countdownSizes.value]
    urls = items[itemId][ConcatcKeys.countdownphotoUrls.value]

    if supermarket == SupportedStores.newWorld:
        names = items[itemId][ConcatcKeys.newWorldItemNames.value]
        sizes = items[itemId][ConcatcKeys.newWorldSizes.value]
        for key in names.keys():
            for index in range(0, len(names[key])):
                if names[key][index] == dictionary[OutputJsonKeys.name.value] and \
                        dictionary[OutputJsonKeys.size.value] == sizes[key][index]:
                    return

        prices = items[itemId][ConcatcKeys.newWorldPrices.value]
        urls = items[itemId][ConcatcKeys.newWorldphotoUrls.value]

    elif supermarket == SupportedStores.packNSave:
        names = items[itemId][ConcatcKeys.packNSaveItemNames.value]
        sizes = items[itemId][ConcatcKeys.packNSaveSizes.value]
        for key in names.keys():
            for index in range(0, len(names[key])):
                if names[key][index] == dictionary[OutputJsonKeys.name.value] and \
                        dictionary[OutputJsonKeys.size.value] == sizes[key][index]:
                    return

        prices = items[itemId][ConcatcKeys.packNSavePrices.value]
        urls = items[itemId][ConcatcKeys.packNSavephotoUrls.value]

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

    items[itemId][ConcatcKeys.category.value] = concatCategory(
        items[itemId][ConcatcKeys.category.value], dictionary[OutputJsonKeys.category.value])


def clusterData():
    threshold = 85
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
    for brand in allCommonKeys:
        packNSaveMappedKey = packNSaveKeyMap[brand]
        newWorldMappedKey = newWorldKeyMap[brand]
        countdownBrand = countdownKeyMap[brand]

        packNSaveItems = packNSaveDict[packNSaveMappedKey]
        newWorldItems = newWorldDict[newWorldMappedKey]
        countdownItems = countdownDict[countdownBrand]
        previousNames = []
        for countdownItem in countdownItems:
            countdownName = finalCategories.transformItem(countdownItem[OutputJsonKeys.name.value], stopSet)
            countdownId = countdownName
            if brand.lower() not in countdownId.lower():
                countdownId += f' {brand}'

            for prevName in previousNames:
                if getRatio(prevName[0], countdownName) > threshold:
                    countdownId = prevName[-1]
                    break
            previousNames.append((countdownName, countdownId))
            countdownId = ' '.join(sorted(countdownId.split(' ')))
            _populateItem(items,
                          countdownItem,
                          countdownId.lower(),
                          countdownBrand,
                          SupportedStores.countdown)

            itemTuples = [(newWorldItems, SupportedStores.newWorld), (packNSaveItems, SupportedStores.packNSave)]
            for itemTuple in itemTuples:
                itemsList, supportedStore = itemTuple
                for otherItem in itemsList:
                    otherItemName = finalCategories.transformItem(otherItem[OutputJsonKeys.name.value], stopSet)
                    itemExists = getRatio(otherItemName, countdownName) > threshold
                    itemId = otherItemName
                    if itemExists:
                        itemId = countdownId
                    elif brand.lower() not in itemId.lower():
                        itemId += f' {brand}'
                    itemId = ' '.join(sorted(itemId.split(' ')))
                    _populateItem(items,
                                  otherItem,
                                  itemId.lower(),
                                  countdownBrand,
                                  supportedStore)

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
        for brand in keys:
            supermarket1Dict, supermarket1Name, supermarket1KeyMap = supermarket1Tuple
            supermarket2Dict, supermarket2Name, supermarket2KeyMap = supermarket2Tuple
            supermarket1MappedBrand = supermarket1KeyMap[brand]
            supermarket2MappedBrand = supermarket2KeyMap[brand]
            supermarket1PreviousItemNames = []
            for supermarket1Item in supermarket1Dict[supermarket1MappedBrand]:
                supermarket1ItemName = finalCategories.transformItem(supermarket1Item[OutputJsonKeys.name.value],
                                                                     stopSet)
                supermarket1Id = supermarket1ItemName
                if brand.lower() not in supermarket1Id.lower():
                    supermarket1Id += f' {brand}'
                for prevName in supermarket1PreviousItemNames:
                    if getRatio(prevName[0], supermarket1ItemName) > threshold:
                        supermarket1Id = prevName[-1]
                        break
                supermarket1PreviousItemNames.append((supermarket1ItemName, supermarket1Id))
                supermarket1Id = ' '.join(sorted(supermarket1Id.split(' ')))
                _populateItem(items,
                              supermarket1Item,
                              supermarket1Id.lower(),
                              supermarket1MappedBrand,
                              supermarket1Name)

                for supermarket2Item in supermarket2Dict[supermarket2MappedBrand]:
                    supermarket2ItemName = finalCategories.transformItem(supermarket2Item[OutputJsonKeys.name.value],
                                                                         stopSet)
                    itemExists = getRatio(supermarket2ItemName, supermarket1ItemName) > threshold
                    itemId = supermarket2ItemName
                    if itemExists:
                        itemId = supermarket1Id
                    elif brand.lower() not in itemId.lower():
                        itemId += f' {brand}'
                    itemId = ' '.join(sorted(itemId.split(' ')))
                    _populateItem(items,
                                  supermarket2Item,
                                  itemId.lower(),
                                  supermarket1MappedBrand,
                                  supermarket2Name)

    supermarketTuples = [(countdownKeys, countdownDict, SupportedStores.countdown, countdownKeyMap),
                         (newWorldKeys, newWorldDict, SupportedStores.newWorld, newWorldKeyMap),
                         (packNSaveKeys, packNSaveDict, SupportedStores.packNSave, packNSaveKeyMap)]

    for supermarketTuple in supermarketTuples:
        supermarketKeys, supermarketDict, supermarketName, supermarketKeyMap = supermarketTuple
        for brand in supermarketKeys:
            mappedBrand = supermarketKeyMap[brand]
            previousNames = []
            for superMarketItem in supermarketDict[mappedBrand]:
                superMarketName = finalCategories.transformItem(superMarketItem[OutputJsonKeys.name.value], stopSet)
                supermarketId = superMarketName
                if brand.lower() not in supermarketId.lower():
                    supermarketId += f' {brand}'
                for prevName in previousNames:
                    if getRatio(prevName[0], superMarketName) > threshold:
                        supermarketId = prevName[-1]
                        break
                previousNames.append((superMarketName, supermarketId))
                supermarketId = ' '.join(sorted(supermarketId.split(' ')))
                _populateItem(items,
                              superMarketItem,
                              supermarketId.lower(),
                              mappedBrand,
                              supermarketName)

    print("cluster done")
    writeItemsToDB(items)


ratioCache = {}


def getRatio(name1, name2):
    name1 = name1.lower()
    name2 = name2.lower()
    key = tuple(sorted((name1, name2)))
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
