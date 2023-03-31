import json

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
    packNSaveFile = open("packNSaveData.json")

    stopWordsFile = open("stopWords.json")
    stopWordsString = stopWordsFile.read()
    stopWordsFile.close()
    stopWordsList = json.loads(stopWordsString)["nonKeyWords"]
    stopSet = set(stopWordsList)

    coutdownString = countdownFile.read()
    newWorldString = newWorldFile.read()
    packNSaveString = packNSaveFile.read()

    countdownDict = json.loads(coutdownString)
    newWorldDict = json.loads(newWorldString)
    packNSaveDict = json.loads(packNSaveString)

    nwK = {}
    psK = {}

    for key in newWorldDict.keys():
        nwK[finalCategories.transformToKey(key)] = key

    for key in packNSaveDict.keys():
        psK[finalCategories.transformToKey(key)] = key
    items = {}

    for ck in countdownDict.keys():
        ckm = finalCategories.transformToKey(ck)
        if ckm in nwK:
            for coutDownItem in countdownDict[ck]:
                countdownName = finalCategories.transformItem(coutDownItem["name"], stopSet)
                if countdownName in items:
                    items[countdownName][ConcatcKeys.countdownItems.value].append(coutDownItem["name"])
                    items[countdownName][ConcatcKeys.countdownPrice.value].append(coutDownItem["price"])
                else:
                    items[countdownName] = {}
                    items[countdownName][ConcatcKeys.countdownItems.value] = [coutDownItem["name"]]
                    items[countdownName][ConcatcKeys.countdownPrice.value] = [coutDownItem["price"]]
                    items[countdownName][ConcatcKeys.newWorldPrice.value] = []
                    items[countdownName][ConcatcKeys.newWorldItems.value] = []
                    items[countdownName][ConcatcKeys.packNSaveItems.value] = []
                    items[countdownName][ConcatcKeys.packNSavePrice.value] = []
                    items[countdownName][ConcatcKeys.category.value] = coutDownItem["category"]

                for newWorldItem in newWorldDict[nwK[ckm]]:
                    newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
                    if countdownName in newWorldName or newWorldName in countdownName or newWorldName == countdownName:
                        items[countdownName][ConcatcKeys.newWorldPrice.value].append(newWorldItem["price"])
                        items[countdownName][ConcatcKeys.newWorldItems.value].append(newWorldItem["name"])
                    else:
                        items[newWorldName] = {}
                        items[newWorldName][ConcatcKeys.newWorldItems.value] = [newWorldItem["name"]]
                        items[newWorldName][ConcatcKeys.newWorldPrice.value] = [newWorldItem["price"]]
                        items[newWorldName][ConcatcKeys.countdownItems.value] = []
                        items[newWorldName][ConcatcKeys.countdownPrice.value] = []
                        items[newWorldName][ConcatcKeys.packNSaveItems.value] = []
                        items[newWorldName][ConcatcKeys.packNSavePrice.value] = []
                        items[newWorldName][ConcatcKeys.category.value] = newWorldItem["category"]
        if ckm in psK:
            for coutDownItem in countdownDict[ck]:
                countdownName = finalCategories.transformItem(coutDownItem["name"], stopSet)
                if countdownName in items:
                    items[countdownName][ConcatcKeys.countdownItems.value].append(coutDownItem["name"])
                    items[countdownName][ConcatcKeys.countdownPrice.value].append(coutDownItem["price"])
                else:
                    items[countdownName] = {}
                    items[countdownName][ConcatcKeys.countdownItems.value] = [coutDownItem["name"]]
                    items[countdownName][ConcatcKeys.countdownPrice.value] = [coutDownItem["price"]]
                    items[countdownName][ConcatcKeys.newWorldPrice.value] = []
                    items[countdownName][ConcatcKeys.newWorldItems.value] = []
                    items[countdownName][ConcatcKeys.packNSaveItems.value] = []
                    items[countdownName][ConcatcKeys.packNSavePrice.value] = []
                    items[countdownName][ConcatcKeys.category.value] = coutDownItem["category"]

                for packNSaveItem in packNSaveDict[psK[ckm]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem["name"], stopSet)
                    if countdownName in pakNSaveName or pakNSaveName in countdownName or pakNSaveName == countdownName:
                        items[countdownName][ConcatcKeys.packNSavePrice.value].append(packNSaveItem["price"])
                        items[countdownName][ConcatcKeys.packNSaveItems.value].append(packNSaveItem["name"])
                    else:
                        items[pakNSaveName] = {}
                        items[pakNSaveName][ConcatcKeys.newWorldItems.value] = []
                        items[pakNSaveName][ConcatcKeys.newWorldPrice.value] = []
                        items[pakNSaveName][ConcatcKeys.countdownItems.value] = []
                        items[pakNSaveName][ConcatcKeys.countdownPrice.value] = []
                        items[pakNSaveName][ConcatcKeys.packNSaveItems.value] = [packNSaveItem["name"]]
                        items[pakNSaveName][ConcatcKeys.packNSavePrice.value] = [packNSaveItem["price"]]
                        items[pakNSaveName][ConcatcKeys.category.value] = packNSaveItem["category"]

    for key in nwK.keys():
        if key in psK and key not in items.keys():
            for newWorldItem in newWorldDict[nwK[key]]:
                newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
                if newWorldName in items:
                    items[newWorldName][ConcatcKeys.newWorldItems.value].append(newWorldItem["name"])
                    items[newWorldName][ConcatcKeys.newWorldPrice.value].append(newWorldItem["price"])
                else:
                    items[newWorldName] = {}
                    items[newWorldName][ConcatcKeys.countdownItems.value] = []
                    items[newWorldName][ConcatcKeys.countdownPrice.value] = []
                    items[newWorldName][ConcatcKeys.newWorldPrice.value] = [newWorldItem["price"]]
                    items[newWorldName][ConcatcKeys.newWorldItems.value] = [newWorldItem["name"]]
                    items[newWorldName][ConcatcKeys.packNSaveItems.value] = []
                    items[newWorldName][ConcatcKeys.packNSavePrice.value] = []
                    items[newWorldName][ConcatcKeys.category.value] = newWorldItem["category"]

                for packNSaveItem in packNSaveDict[psK[key]]:
                    pakNSaveName = finalCategories.transformItem(packNSaveItem["name"], stopSet)
                    if newWorldName in pakNSaveName or pakNSaveName in newWorldName or pakNSaveName == newWorldName:
                        items[newWorldName][ConcatcKeys.packNSavePrice.value].append(packNSaveItem["price"])
                        items[newWorldName][ConcatcKeys.packNSaveItems.value].append(packNSaveItem["name"])
                    else:
                        items[pakNSaveName] = {}
                        items[pakNSaveName][ConcatcKeys.newWorldItems.value] = []
                        items[pakNSaveName][ConcatcKeys.newWorldPrice.value] = []
                        items[pakNSaveName][ConcatcKeys.countdownItems.value] = []
                        items[pakNSaveName][ConcatcKeys.countdownPrice.value] = []
                        items[pakNSaveName][ConcatcKeys.packNSaveItems.value] = [packNSaveItem["name"]]
                        items[pakNSaveName][ConcatcKeys.packNSavePrice.value] = [packNSaveItem["price"]]
                        items[pakNSaveName][ConcatcKeys.category.value] = packNSaveItem["category"]

    for ck in countdownDict.keys():
        ckm = finalCategories.transformToKey(ck)
        if ckm not in items.keys():
            for coutDownItem in countdownDict[ck]:
                countdownName = finalCategories.transformItem(coutDownItem["name"], stopSet)
                if countdownName in items:
                    items[countdownName][ConcatcKeys.countdownItems.value].append(coutDownItem["name"])
                    items[countdownName][ConcatcKeys.countdownPrice.value].append(coutDownItem["price"])
                else:
                    items[countdownName] = {}
                    items[countdownName][ConcatcKeys.countdownItems.value] = [coutDownItem["name"]]
                    items[countdownName][ConcatcKeys.countdownPrice.value] = [coutDownItem["price"]]
                    items[countdownName][ConcatcKeys.newWorldPrice.value] = []
                    items[countdownName][ConcatcKeys.newWorldItems.value] = []
                    items[countdownName][ConcatcKeys.packNSaveItems.value] = []
                    items[countdownName][ConcatcKeys.packNSavePrice.value] = []
                    items[countdownName][ConcatcKeys.category.value] = coutDownItem["category"]


    for nwk in newWorldDict.keys():
        nwkm = finalCategories.transformToKey(nwk)
        if nwkm not in items.keys():
            for newWorldItem in newWorldDict[nwk]:
                newWorldName = finalCategories.transformItem(newWorldItem["name"], stopSet)
                if newWorldName in items:
                    items[newWorldName][ConcatcKeys.newWorldItems.value].append(newWorldItem["name"])
                    items[newWorldName][ConcatcKeys.newWorldPrice.value].append(newWorldItem["price"])
                else:
                    items[newWorldName] = {}
                    items[newWorldName][ConcatcKeys.countdownItems.value] = []
                    items[newWorldName][ConcatcKeys.countdownPrice.value] = []
                    items[newWorldName][ConcatcKeys.newWorldPrice.value] = [newWorldItem["price"]]
                    items[newWorldName][ConcatcKeys.newWorldItems.value] = [newWorldItem["name"]]
                    items[newWorldName][ConcatcKeys.packNSaveItems.value] = []
                    items[newWorldName][ConcatcKeys.packNSavePrice.value] = []
                    items[newWorldName][ConcatcKeys.category.value] = newWorldItem["category"]


    for psk in packNSaveDict.keys():
        pskm = finalCategories.transformToKey(psk)
        if pskm not in items.keys():
            for pakNSaveItem in packNSaveDict[psk]:
                pakNSaveName = finalCategories.transformItem(pakNSaveItem["name"], stopSet)
                if pakNSaveName in items:
                    items[pakNSaveName][ConcatcKeys.packNSaveItems.value].append(pakNSaveItem["name"])
                    items[pakNSaveName][ConcatcKeys.packNSavePrice.value].append(pakNSaveItem["price"])
                else:
                    items[pakNSaveName] = {}
                    items[pakNSaveName][ConcatcKeys.countdownItems.value] = []
                    items[pakNSaveName][ConcatcKeys.countdownPrice.value] = []
                    items[pakNSaveName][ConcatcKeys.newWorldPrice.value] = []
                    items[pakNSaveName][ConcatcKeys.newWorldItems.value] = []
                    items[pakNSaveName][ConcatcKeys.packNSaveItems.value] = [pakNSaveItem["name"]]
                    items[pakNSaveName][ConcatcKeys.packNSavePrice.value] = [pakNSaveItem["price"]]
                    items[pakNSaveName][ConcatcKeys.category.value] = pakNSaveItem["category"]
    count = 1
    for item in items.values():
        # :
        #     print(f"CountDown: {item[ConcatcKeys.countdownItems.value]}")

        if item[ConcatcKeys.packNSaveItems.value] and item[ConcatcKeys.newWorldItems.value] and item[ConcatcKeys.countdownItems.value]:
            print(count)
            print(f"NewWorld: {item[ConcatcKeys.newWorldItems.value]}")
            print(f"NewWorld: {item[ConcatcKeys.newWorldPrice.value]}")
            print(f"PackNSave: {item[ConcatcKeys.packNSaveItems.value]}")
            print(f"PackNSave: {item[ConcatcKeys.packNSavePrice.value]}")
            print(f"CountDown: {item[ConcatcKeys.countdownItems.value]}")
            print(f"CountDown: {item[ConcatcKeys.countdownPrice.value]}")
            print(item[ConcatcKeys.category.value])
            print("-"*100)
            count += 1


    countdownFile.close()
    newWorldFile.close()
    packNSaveFile.close()
clusterData()
