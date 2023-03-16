import sys

import requests
import re
import json
from enum import Enum
class CountdownKeys(Enum):
    products = "products"
    items = "items"

class CountdownItemKeys(Enum):
    name = "name"
    price = "price"
    size = "size"
    salePrice = "salePrice"
    volumeSize = "volumeSize"
    barcode = "barcode"
class Apis:
    _countDownHeaders = {
        'Host': 'www.countdown.co.nz',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/plain, /',
        'X-Requested-With': 'OnlineShopping.WebApp',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Referer': 'https://www.countdown.co.nz/shop/specials?page=5&inStockProductsOnly=true',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    }
    def fetchCountdownItems(self):
        #lastPage = self._getCountdownLastPage()
        for pageNumber in range(1, 1 + 1):
            response = requests.get(
                f'https://www.countdown.co.nz/api/v1/products?target=specials&page={pageNumber}',
                headers=self._countDownHeaders)
            res = json.loads(response.text)
            items = res[CountdownKeys.products.value][CountdownKeys.items.value]
            for item in items:
                print(CountdownItemKeys.barcode.value, item[CountdownItemKeys.barcode.value])
                print(CountdownItemKeys.name.value, item[CountdownItemKeys.name.value])
                print(CountdownItemKeys.price.value, item[CountdownItemKeys.price.value][CountdownItemKeys.salePrice.value])
                print(CountdownItemKeys.size.value, item[CountdownItemKeys.size.value][CountdownItemKeys.volumeSize.value])
    def _getCountdownLastPage(self) -> int:
        maxSupoortedPages = 300
        response = requests.get(f'https://www.countdown.co.nz/api/v1/products?target=specials&page={maxSupoortedPages}',
                         headers = self._countDownHeaders)
        extracted = re.findall(r'and [0-9]+', response.text)
        if len(extracted) > 0:
            number = str(extracted[0]).strip("and ")
            return int(number)

        return maxSupoortedPages
