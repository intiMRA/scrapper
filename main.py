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

    dictionary: {str: [{str: str}]} = {}
    categories: [str] = []
    for i in nw:
        ar = i.split(",")
        category = ar[2].replace("'", "").strip(" ")
        if category not in dictionary.keys():
            categories.append(category)
            dictionary[category] = []
        dictionary[category].append({"name": ar[0], "price": ar[1]})

    for i in cd:
        ar = i.split(",")
        category = ar[2].replace("'", "").strip(" ")
        if category not in dictionary.keys():
            categories.append(category)
            dictionary[category] = []
        dictionary[category].append({"name": ar[0], "price": ar[1]})

    clusterst = clusterWords(categories)
    for i in range(0, len(clusterst)):
        print(i + 1)
        count = -1
        cat = ""
        for c in clusterst[i]:
            clusterItems = dictionary[c]
            if len(dictionary[c]) > count:
                cat = c
                count = len(dictionary[c])
            for item in clusterItems:
                print(item["name"], item["price"])
        print(cat.upper())
        print("-"*100)

clusterData()
