from flask import Flask, request
import SupermaketItems
from enum import Enum
from waitress import serve

app = Flask(__name__)


class ParameterKeys(Enum):
    lat = "lat"
    long = "long"
    radius = "radius"
    packNSaveIds = "packNSaveIds"
    newWorldIds = "newWorldIds"
    query = "query"
    categories = "categories"


@app.get('/items/<page>')
def getPage(page):
    args = request.args.to_dict()
    newWorldIds = args[ParameterKeys.newWorldIds.value].split(",")
    packNSaveIds = args[ParameterKeys.packNSaveIds.value].split(",")
    return SupermaketItems.fetchPage(page, newWorldIds, packNSaveIds)


@app.get('/items/search')
def searchItems():
    args = request.args.to_dict()
    newWorldIds = args[ParameterKeys.newWorldIds.value].split(",")
    packNSaveIds = args[ParameterKeys.packNSaveIds.value].split(",")
    query = args[ParameterKeys.query.value]
    return SupermaketItems.searchForItems(query, newWorldIds, packNSaveIds)


@app.route('/items/category')
def getCategories():
    args = request.args.to_dict()
    newWorldIds = args[ParameterKeys.newWorldIds.value].split(",")
    packNSaveIds = args[ParameterKeys.packNSaveIds.value].split(",")
    categories = args[ParameterKeys.categories.value].split(",")
    return SupermaketItems.fetchCategories(categories, newWorldIds, packNSaveIds)

@app.route('/items/categoryNames')
def getCategoryNames():
    return SupermaketItems.fetchCategoryNames()
@app.route('/stores')
def getStores():
    args = request.args.to_dict()
    lat = args[ParameterKeys.lat.value]
    long = args[ParameterKeys.long.value]
    radius = args[ParameterKeys.radius.value]
    return SupermaketItems.fetchStores(lat, long, radius)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
