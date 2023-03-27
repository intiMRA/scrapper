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
    cdf = open("countDownData.csv")
    nwf = open("newWorldData.csv")
    stopWordsf = open("stopWords.json")
    stopWords = stopWordsf.read()
    stopWordsf.close()
    stopWordsList = json.loads(stopWords)["nonKeyWords"]
    stopDict = {}
    for s in stopWordsList:
        stopDict[s] = s
    cd = cdf.readlines()
    nw = nwf.readlines()
    items = []
    for i in cd:
        item = i.split(",")
        for i2 in nw:
            item2 = i2.split(",")
            name1 = finalCategories.transformToKey(item[0], stopDict)
            name2 = finalCategories.transformToKey(item2[0], stopDict)
            cats1 = item[2].split("@")
            cats2 = item2[2].split("@")
            brand1 = finalCategories.transformToKey(item[3])
            brand2 = finalCategories.transformToKey(item2[3])
            v = False
            if name1 == name2 or name2 in name1 or name1 in name2:
                v = True

            if v and brand2 == brand1:
                s = "name: " + name1 + " , " + name2 + "brand: " + brand1 + " , " + brand2
                items.append(s)
    for i in items:
        print(i)

    cdf.close()
    nwf.close()
clusterData()
