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

    dictionary: {str: {str: {str: str}}} = {}
    for i in nw:
        ar = i.split(",")
        category = ar[2].replace("'", "").replace("\n", "")
        if category not in dictionary.keys():
            dictionary[category] = {ar[0].replace("&", "").replace(" ", ""): {"nwPrice": ar[1], "name": ar[0]}}
        else:
            if ar[0].replace("&", "").replace(" ", "") in dictionary[category]:
                dictionary[category][ar[0].replace("&", "").replace(" ", "")]["nwPrice"] = ar[1]
            else:
                dictionary[category][ar[0].replace("&", "").replace(" ", "")] = {"nwPrice": ar[1], "name": ar[0]}

    for i in cd:
        ar = i.split(",")
        category = ar[2].replace("'", "").replace("\n", "")
        if category not in dictionary.keys():
            dictionary[category] = {ar[0].replace("&", "").replace(" ", ""): {"cdPrice": ar[1], "name": ar[0]}}
        else:
            if ar[0].replace("&", "").replace(" ", "") in dictionary[category]:
                dictionary[category][ar[0].replace("&", "").replace(" ", "")]["cdPrice"] = ar[1]
            else:
                dictionary[category][ar[0].replace("&", "").replace(" ", "")] = {"cdPrice": ar[1], "name": ar[0]}

    for parentKey in categories.keys():
        print(parentKey + "\n")
        for key in categories[parentKey]:
            key = key.replace("'", "").strip(" ")
            if key in dictionary:
                for subKeys in dictionary[key].keys():
                    item = dictionary[key][subKeys]
                    cdp = "-1"
                    nwp = "-1"
                    if "cdPrice" in item.keys():
                        cdp = item["cdPrice"]

                    if "nwPrice" in item.keys():
                        nwp = item["nwPrice"]
                    print(item["name"] + ", " + "nw: " + nwp + "cd: " + cdp + "\n")
        print("-"*100)
Apis().fetchCountdownItems()
