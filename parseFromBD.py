from Database import Database
from Database import ConcatcKeys
import json

def fetchAll():
    db = Database()
    db.startConnection()
    items = db.fetchAllItems()
    db.closeConnection()
    output = _parseToDict(items)
    for o in output:
        print(o)

def _parseToDict(items) -> list:
    output = []
    for item in items:
        outPutItem = {}
        for index, key in enumerate(ConcatcKeys):
            if index > 12:
                outPutItem[key.value] = item[index]
            else:
                outPutItem[key.value] = item[index].split("@")
        output.append(outPutItem)
    return output

def fetchCategories():
    db = Database()
    db.startConnection()
    items = db.fetchItemsByCategory(["drink", "meat"])
    db.closeConnection()
    output = _parseToDict(items)
    for o in output:
        print(o)