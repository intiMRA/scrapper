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
    cd = cdf.readlines()
    nw = nwf.readlines()
    for i in cd:
        item = i.split(",")
        for i2 in nw:
            item2 = i2.split(",")
            name1 = finalCategories.transformToKey(item[0])
            name2 = finalCategories.transformToKey(item2[0])
            cats1 = item[2].split("@")
            cats2 = item2[2].split("@")
            brand1 = finalCategories.transformToKey(item[3])
            brand2 = finalCategories.transformToKey(item2[3])
            v = False
            if name1 == name2:
                v = True
            if brand1 == brand2:
                v = True

            if v:
                print("name: " + name1 + " , " + name2)
                print("brand: " + brand1 + " , " + brand2)
                print("-"*100)

    cdf.close()
    nwf.close()
clusterData()
