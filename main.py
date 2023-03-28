import json

from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
import finalCategories

class SupportedStores(Enum):
    newWorld = "NewWorld"
    PackNSave = "packNSave"
    countdown = "Countdown"


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
                items[name1] = {"name": [coutDownItem["name"]], "nwp": "0", "cdp": coutDownItem["price"], "category": coutDownItem["category"]}
                for newWorldItem in newWorldDict[nwK[ckm]]:
                    name2 = finalCategories.transformItem(newWorldItem["name"], stopSet)
                    if name1 in name2 or name2 in name1 or name2 == name1:
                        items[name1]["nwp"] = newWorldItem["price"]
                        items[name1]["name"].append(newWorldItem["name"])
                    else:
                        items[name2] = {"name": [newWorldItem["name"]], "nwp": newWorldItem["price"], "cdp": "0",
                                        "category": newWorldItem["category"]}
    for item in items.values():
        print(item["name"])
        print(item["category"])
        print("-"*100)


    countdownFile.close()
    newWorldFile.close()
clusterData()
