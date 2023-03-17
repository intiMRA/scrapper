
from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from Cluster import Cluster
class SupportedStores(Enum):
    newWorld = "NewWorld"
    PackNSave = "packNSave"
    countdown = "Countdown"
def createTables():
    db = Database()
    db.startConnection()
    db.testConnection()
    for store in SupportedStores:
        db.createTable(tableName = store.value, tableParameters= ["itemName VARCHAR(255)", "itemPrice VARCHAR(255)"])
    db.printTables()
    db.closeConnection()

def fetchData():
    api = Apis()
    api.fetchCountdownItems()

def clusterData():
    cd = open("countDownData.csv")
    nw = open("newWorldData.csv")

    nwDict = {}
    nwArr = []
    for i in nw:
        ar = i.split(",")
        nwDict[ar[0]] = ar[1]
        nwArr.append(str(ar[0]))

    cdDict = {}
    cdArr = []

    for i in cd:
        ar = i.split(",")
        cdDict[ar[0]] = ar[1]
        cdArr.append(str(ar[0]))
    print(cdArr + nwArr)
    Cluster().clusterWords(cdArr + nwArr)

Database().testConnection()