from Database import Database
from Database import ConcatcKeys
import json


def fetchAll():
    db = Database()
    db.startConnection()
    items = db.fetchAllItems()
    db.closeConnection()
    output = _parseToDict(items)
    return output


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


def fetchCategories(categories: str):
    db = Database()
    db.startConnection()
    items = db.fetchItemsByCategory(categories.split(","))
    db.closeConnection()
    output = _parseToDict(items)
    return output


class SupermaketItems:
    pass
