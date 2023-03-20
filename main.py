from Database import Database
from enum import Enum
from SuperMarketsApis import Apis
from finalCategories import categories


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

    dictionary: {str: [{str: str}]} = {}

    for i in nw:
        ar = i.split(",")
        category = ar[2].replace("'", "").replace("\n", "")
        if category not in dictionary.keys():
            dictionary[category] = []
        dictionary[category].append({"name": ar[0], "price": ar[1]})

    for i in cd:
        ar = i.split(",")
        category = ar[2].replace("'", "").replace("\n", "")
        if category not in dictionary.keys():
            dictionary[category] = []
        dictionary[category].append({"name": ar[0], "price": ar[1]})

    for parentKey in categories.keys():
        print(parentKey + "\n")
        for key in categories[parentKey]:
            key = key.replace("'", "").strip(" ")
            if key in dictionary:
                for item in dictionary[key]:
                    print(item["name"] + ", " + item["price"] + "\n")
        print("-"*100)
clusterData()
