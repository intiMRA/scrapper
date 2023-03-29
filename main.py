import json

from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
import finalCategories

class SupportedStores(Enum):
    newWorld = "NewWorld"
    PackNSave = "packNSave"
    countdown = "Countdown"

class ConcatcKeys(Enum):
    newWorldItems = "newWorldItems"
    PackNSaveItems = "PackNSaveItems"
    countdownItems = "countdownItems"
    newWorldPrice = "newWorldPrice"
    PackNSavePrice = "PackNSavePrice"
    countdownPrice = "countdownPrice"
    category = "category"
    brand = "brand"

def createTables():
    db = Database()
    db.startConnection()
    db.testConnection()
    for store in SupportedStores:
        db.createTable(tableName=store.value, tableParameters=["itemName VARCHAR(255)", "itemPrice VARCHAR(255)"])
    db.printTables()
    db.closeConnection()


def fetchData():
    api = Apis()
    api.fetchNewworldItems()
    api.fetchCountdownItems()


def clusterData():
    countdownFile = open("countDownData.json")
    newWorldFile = open("newWorldData.json")

    stopWordsFile = open("stopWords.json")
    stopWordsString = stopWordsFile.read()
    stopWordsFile.close()
    stopWordsList = json.loads(stopWordsString)["nonKeyWords"]
    stopSet = set(stopWordsList)

    coutdownString = countdownFile.read()
    newWorldString = newWorldFile.read()

    countdownDict = json.loads(coutdownString)
    newWorldDict = json.loads(newWorldString)
    nwK = {}
    count = 0
    for key in newWorldDict.keys():
        nwK[finalCategories.transformToKey(key)] = key
    items = {}
    for ck in countdownDict.keys():
        ckm = finalCategories.transformToKey(ck)
        if ckm in nwK:
            for coutDownItem in countdownDict[ck]:
                name1 = finalCategories.transformItem(coutDownItem["name"], stopSet)
                if name1 in items:
                    items[name1][ConcatcKeys.countdownItems.value].append(coutDownItem["name"])
                    items[name1][ConcatcKeys.countdownPrice.value].append(coutDownItem["price"])
                else:
                    items[name1] = {}
                    items[name1][ConcatcKeys.countdownItems.value] = [coutDownItem["name"]]
                    items[name1][ConcatcKeys.countdownPrice.value] = [coutDownItem["price"]]
                    items[name1][ConcatcKeys.newWorldPrice.value] = []
                    items[name1][ConcatcKeys.newWorldItems.value] = []
                    items[name1][ConcatcKeys.category.value] = coutDownItem["category"]

                for newWorldItem in newWorldDict[nwK[ckm]]:
                    name2 = finalCategories.transformItem(newWorldItem["name"], stopSet)
                    if name1 in name2 or name2 in name1 or name2 == name1:
                        items[name1][ConcatcKeys.newWorldPrice.value].append(newWorldItem["price"])
                        items[name1][ConcatcKeys.newWorldItems.value].append(newWorldItem["name"])
                    else:
                        items[name2] = {}
                        items[name2][ConcatcKeys.newWorldItems.value] = [newWorldItem["name"]]
                        items[name2][ConcatcKeys.newWorldPrice.value] = [newWorldItem["price"]]
                        items[name2][ConcatcKeys.countdownItems.value] = []
                        items[name2][ConcatcKeys.countdownPrice.value] = []
                        items[name2][ConcatcKeys.category.value] = newWorldItem["category"]

    for item in items.values():
        if item[ConcatcKeys.countdownItems.value]:
            print(item[ConcatcKeys.countdownItems.value])
        if item[ConcatcKeys.newWorldItems.value]:
            print(item[ConcatcKeys.newWorldItems.value])
        print(item[ConcatcKeys.category.value])
        print("-"*100)


    countdownFile.close()
    newWorldFile.close()
clusterData()
