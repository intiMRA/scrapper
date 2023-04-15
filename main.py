from flask import Flask, request
import SupermaketItems
from enum import Enum

app = Flask(__name__)


class ParameterKeys(Enum):
    lat = "lat"
    long = "long"
    radius = "radius"


@app.get('/items/<page>')
def getPage(page):
    return {'items': SupermaketItems.fetchPage(page)}


@app.route('/items/<categories>')
def getCategories(categories):
    return SupermaketItems.fetchCategories(categories)


@app.route('/stores')
def getStores():
    args = request.args.to_dict()
    try:
        lat = args[ParameterKeys.lat.value]
        long = args[ParameterKeys.long.value]
        radius = args[ParameterKeys.radius.value]
        return SupermaketItems.fetchStores(lat, long, radius)
    except:
        return "error", 400


if __name__ == '__main__':
    app.run()  # run our Flask app
