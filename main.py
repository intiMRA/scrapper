from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from Cluster import clusterWords


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
    api.fetchCountdownItems()
    api.fetchNewworldItems()


def clusterData():
    cd = open("countDownData.csv")
    nw = open("newWorldData.csv")

    nwDict = {}
    nwArr = []
    for i in nw:
        ar = i.split(",")
        nwDict[ar[0]] = ar[1]
        if ar[2] not in nwArr:
            nwArr.append(str(ar[2]))

    cdDict = {}
    cdArr = []

    for i in cd:
        ar = i.split(",")
        cdDict[ar[0]] = ar[1]
        if ar[2] not in cdArr:
            cdArr.append(str(ar[2]))

    clusterWords(cdArr + nwArr)

clusterData()
