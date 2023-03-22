import requests
import time
import json
from enum import Enum
from dotenv import load_dotenv
import os
from pathlib import Path
import finalCategories

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class CountdownKeys(Enum):
    products = "products"
    items = "items"
    dasFacets = "dasFacets"


class NewWorldKeys(Enum):
    products = "hits"
    storesAvailable = "onPromotion"
    accessToken = "accessToken"
    access_token = "access_token"
    refreshToken = "refreshToken"
    refresh_token = "refresh_token"


class NewWorldItemKeys(Enum):
    size = "weightDisplayName"
    name = "DisplayName"
    price = "prices"
    brand = "brand"
    category = "category1"


class CountdownItemIgnoreKeys(Enum):
    adds = "PromoTile"


class CountdownItemKeys(Enum):
    name = "name"
    price = "price"
    size = "size"
    salePrice = "salePrice"
    volumeSize = "volumeSize"
    brand = "brand"
    type = "type"
    category = "category"


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
        'Referer': 'https://www.countdown.co.nz/shop',
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

    def _fetchDepartments(self) -> [{str: str}]:
        url = "https://www.countdown.co.nz/api/v1/products?target=specials"
        response = requests.get(
            url,
            headers=self._countDownHeaders)
        ref = json.loads(response.text)
        dasFacets = ref[CountdownKeys.dasFacets.value]
        departments = []
        for cat in dasFacets:
            name = cat[CountdownItemKeys.name.value]
            departments.append({
                CountdownItemKeys.name.value: name,
                CountdownItemKeys.category.value:
                    name.replace(" ", "").replace("&", "-").lower()
            })
        return departments

    def fetchCountdownItems(self):
        departments = self._fetchDepartments()
        countDownDataFile = open("countDownData.csv", mode="w")
        count = 0
        for department in departments:
            url = f'https://www.countdown.co.nz/api/v1/products?dasFilter=Department%3B%3B{department["category"]}%3Bfalse&dasFilter' \
                  "=Aisle%3B%3Bfresh-deals%3Bfalse&target=browse&promo_name=%20-%20Specials%20Hub"
            for pageNumber in range(1, 300):
                response = requests.get(
                    f'{url}&page={pageNumber}',
                    headers=self._countDownHeaders)
                res = json.loads(response.text)
                items = res[CountdownKeys.products.value][CountdownKeys.items.value]
                if len(items) == 0:
                    print("DONE")
                    break
                for item in items:
                    if item[CountdownItemKeys.type.value] == CountdownItemIgnoreKeys.adds.value or CountdownItemKeys.price.value not in item:
                        continue
                    count += 1

                    countDownDataFile.write(
                        f'{item[CountdownItemKeys.name.value]},'
                        f'{item[CountdownItemKeys.price.value][CountdownItemKeys.salePrice.value]},'
                        f'{finalCategories.concatCategories(department[CountdownItemKeys.name.value])},'
                        f'{item[CountdownItemKeys.brand.value]}\n'
                    )
                    if count >= 1000:
                        break
            time.sleep(0.2)
            if count >= 1000:
                break
        countDownDataFile.close()

    def fetchNewworldItems(self):
        storeId = "63cbb6c6-4a0b-448d-aa78-8046692a082c"
        newWorldDataFile = open("newWorldData.csv", mode="w")
        requestBody = '{"query":"","facets":["category1NI","onPromotion"],"attributesToHighlight":[],' \
                      '"sortFacetValuesBy":"alpha","hitsPerPage":"1000","facetFilters":[' \
                      f'"stores:{storeId}",' \
                      f'["onPromotion:{storeId}"],"tobacco:false"]' \
                      '}'
        url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/product/search/MNW?sortOrder=popularity'
        headers = self._newWorldHeaders
        headers["Authorization"] = self._getNewWorldToken()
        response = requests.post(url, headers=self._newWorldHeaders, data=requestBody)
        jsonResponse = json.loads(response.text)
        items = jsonResponse[NewWorldKeys.products.value]
        storeId = storeId.replace("-", "")
        for item in items:
            price = 1
            if storeId in item[NewWorldItemKeys.price.value].keys():
                price = item[NewWorldItemKeys.price.value][storeId]
            brand = "new world"
            if NewWorldItemKeys.brand.value in item.keys():
                brand = item[NewWorldItemKeys.brand.value]
            newWorldDataFile.write(
                f'{item[NewWorldItemKeys.name.value]},'
                f'{price},'
                f'{finalCategories.concatCategories(item[NewWorldItemKeys.category.value][0])},'
                f'{brand}\n'
            )
        newWorldDataFile.close()

    def _getNewWorldToken(self) -> str:
        try:
            refreshTokenFile = open("refreshToken.txt", mode="r")
            url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/users/login/refreshtoken'
            refreshToken = refreshTokenFile.readline(1)
            body = f'"refreshToken":"{refreshToken}"'
            body = "{" + body + "}"
            response = requests.post(url, headers=self._newWorldHeaders, data=body)
            responseJson = json.loads(response.text)
            bearerToken = responseJson[NewWorldKeys.accessToken.value]
            newRefreshToken = responseJson[NewWorldKeys.refreshToken.value]
            refreshTokenFile.close()
            refreshTokenFile = open("refreshToken.txt", mode="w")
            refreshTokenFile.write(newRefreshToken)
            refreshTokenFile.close()
            return f'Bearer {bearerToken}'
        except:
            # log in
            url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/user/login'
            body = '{' + \
                   f'"email":"{os.getenv("EMAIL")}","password":"{os.getenv("EMAIL_PASSWORD")}","banner":"MNW"' + \
                   '}'
            response = requests.post(url, headers=self._newWorldHeaders, data=body)
            responseJson = json.loads(response.text)
            bearerToken = responseJson[NewWorldKeys.access_token.value]
            newRefreshToken = responseJson[NewWorldKeys.refresh_token.value]
            refreshTokenFile = open("refreshToken.txt", mode="w")
            refreshTokenFile.write(newRefreshToken)
            refreshTokenFile.close()
            return f'Bearer {bearerToken}'
