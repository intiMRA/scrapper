import requests
import re
import json
from enum import Enum


class CountdownKeys(Enum):
    products = "products"
    items = "items"


class NewWorldKeys(Enum):
    products = "hits"
    storesAvailable = "onPromotion"
    accessToken = "accessToken"
    refreshToken = "refreshToken"


class NewWorldItemKeys(Enum):
    size = "weightDisplayName"
    name = "DisplayName"
    price = "prices"
    brand = "brand"


class CountdownItemKeys(Enum):
    name = "name"
    price = "price"
    size = "size"
    salePrice = "salePrice"
    volumeSize = "volumeSize"
    barcode = "barcode"
    brand = "brand"


class Apis:
    _countDownHeaders = {
        'Host': 'www.countdown.co.nz',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/plain, /',
        'X-Requested-With': 'OnlineShopping.WebApp',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                      'like Gecko) Mobile/15E148',
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
        'Content-Length': '325',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Content-Type': 'application/json'
    }

    def fetchCountdownItems(self):
        countDownDataFile = open("countDownData.csv", mode="w")
        countDownDataFile.write("name, price\n")
        lastPage = self._getCountdownLastPage()
        for pageNumber in range(1, lastPage + 1):
            response = requests.get(
                f'https://www.countdown.co.nz/api/v1/products?target=specials&page={pageNumber}',
                headers=self._countDownHeaders)
            res = json.loads(response.text)
            items = res[CountdownKeys.products.value][CountdownKeys.items.value]
            for item in items:
                print(item.keys())
                countDownDataFile.write(
                    f'{item[CountdownItemKeys.name.value]},'
                    f'{item[CountdownItemKeys.price.value][CountdownItemKeys.salePrice.value]}\n')
        countDownDataFile.close()

    def fetchNewworldItems(self):
        storeId = "63cbb6c6-4a0b-448d-aa78-8046692a082c"
        newWorldDataFile = open("newWorldData.csv", mode="w")
        newWorldDataFile.write("name, price\n")
        requestBody = '{"query":"","facets":["category1NI","onPromotion"],"attributesToHighlight":[],' \
                      '"sortFacetValuesBy":"alpha","hitsPerPage":"100","facetFilters":[' \
                      f'"stores:{storeId}",' \
                      f'["onPromotion:{storeId}"],"tobacco:false"]' \
                      '}'
        url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/product/search/MNW?sortOrder=popularity'
        headers = self._newWorldHeaders
        headers["Authorization"] = self._getNewWorldToken()
        response = requests.post(url, headers=self._newWorldHeaders, data=requestBody)
        jsonResponse = json.loads(response.text)
        items = jsonResponse[NewWorldKeys.products.value]
        for item in items:
            newWorldDataFile.write(
                f'{item[NewWorldItemKeys.name.value]},'
                f'{item[NewWorldItemKeys.price.value][storeId]}\n')
        newWorldDataFile.close()

    def _getNewWorldToken(self) -> str:
        try:
            refreshTokenFile = open("toke.txt", mode="r")
            url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/users/login/refreshtoken'
            refreshToken = refreshTokenFile.readline(1)
            body = f'"refreshToken":"{refreshToken}"'
            body = "{" + body + "}"
            response = requests.post(url, headers=self._newWorldHeaders, data=body)
            responseJson = json.loads(response.text)
            bearerToken = responseJson[NewWorldKeys.accessToken.value]
            newRefreshToken = responseJson[NewWorldKeys.refreshToken.value]
            refreshTokenFile.close()
            refreshTokenFile = open("toke.txt", mode="w")
            refreshTokenFile.write(newRefreshToken)
            return f'Bearer {bearerToken}'
        except:
            # log in
            return ""

    def _getCountdownLastPage(self) -> int:
        maxSupportedPages = 300
        response = requests.get(f'https://www.countdown.co.nz/api/v1/products?target=specials&page={maxSupportedPages}',
                                headers=self._countDownHeaders)
        extracted = re.findall(r'and [0-9]+', response.text)
        if len(extracted) > 0:
            number = str(extracted[0]).strip("and ")
            return int(number)

        return maxSupportedPages
