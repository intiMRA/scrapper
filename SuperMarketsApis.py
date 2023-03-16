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

    _token = ''

    _newWorldHeaders = {
        'Host': 'api-prod.prod.fsniwaikato.kiwi',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'NewWorldApp/4.4.0 (iOS 16.3.1)',
        'Authorization': f'{_token}',
        'Content-Length': '325',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Content-Type': 'application/json'
    }

    _newWorldRequestBody = '{"query":"","facets":["category1NI","onPromotion"],"attributesToHighlight":[],"sortFacetValuesBy":"alpha","hitsPerPage":"10000","facetFilters":["stores:63cbb6c6-4a0b-448d-aa78-8046692a082c",["onPromotion:63cbb6c6-4a0b-448d-aa78-8046692a082c"],"tobacco:false"]}'

    def fetchCountdownItems(self):
        lastPage = self._getCountdownLastPage()
        for pageNumber in range(1, lastPage + 1):
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
    def fetchNewworldItems(self):
        f = open("out.json", mode="w")
        url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/product/search/MNW?sortOrder=popularity'
        response = requests.post(url, headers=self._newWorldHeaders, data=self._newWorldRequestBody)
        f.write(response.text)
        f.close()

    def _getNewWorldToken(self):
        return
    def _getCountdownLastPage(self) -> int:
        maxSupoortedPages = 300
        response = requests.get(f'https://www.countdown.co.nz/api/v1/products?target=specials&page={maxSupoortedPages}',
                         headers = self._countDownHeaders)
        extracted = re.findall(r'and [0-9]+', response.text)
        if len(extracted) > 0:
            number = str(extracted[0]).strip("and ")
            return int(number)

        return maxSupoortedPages
