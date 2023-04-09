import requests
import json
from enum import Enum
from dotenv import load_dotenv
import os
from pathlib import Path
import finalCategories
import typing
import re

dotenv_path = Path('./venv/.env')
load_dotenv(dotenv_path=dotenv_path)


class SuperMarketAbbreviation(Enum):
    newWorld = "MNW"
    packNSave = "PNS"


class FileNames(Enum):
    newWorldFile = "newWorldData.json"
    packNSaveFile = "packNSaveData.json"
    countdownFile = "countdown.json"


class OutputJsonKeys(Enum):
    name = "name"
    price = "price"
    category = "category"
    photoUrl = "photoUrl"
    brand = "brand"
    size = "size"


class CountdownKeys(Enum):
    products = "products"
    items = "items"
    dasFacets = "dasFacets"


class FoodStuffsKeys(Enum):
    products = "hits"
    storesAvailable = "onPromotion"
    accessToken = "accessToken"
    access_token = "access_token"
    refreshToken = "refreshToken"
    refresh_token = "refresh_token"
    facets = "facets"
    category1NI = "category1NI"


class FoodStuffsItemKeys(Enum):
    size = "weightDisplayName"
    name = "DisplayName"
    price = "prices"
    brand = "brand"
    category = "category1"
    objectID = "objectID"


class CountdownItemIgnoreKeys(Enum):
    adds = "PromoTile"


class CountdownItemKeys(Enum):
    name = "name"
    price = "price"
    size = "size"
    salePrice = "salePrice"
    volumeSize = "volumeSize"
    cupMeasure = "cupMeasure"
    packageType = "packageType"
    unit = "unit"
    brand = "brand"
    type = "type"
    images = "images"
    iconLarge = "big"
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

    _foodStuffsHeaders = ''

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
        countDownDataFile = open("countDownData.json", mode="w")
        countDownDataFile.write("{\n")
        itemDict = {}
        count = 0
        for department in departments:
            url = f'https://www.countdown.co.nz' \
                  f'/api/v1/products?dasFilter=Department%3B%3B{department[CountdownItemKeys.category.value]}%3Bfalse&dasFilter' \
                  "=Aisle%3B%3Bfresh-deals%3Bfalse&target=browse&promo_name=%20-%20Specials%20Hub"
            for pageNumber in range(1, 120):
                response = requests.get(
                    f'{url}&page={pageNumber}',
                    headers=self._countDownHeaders)
                res = json.loads(response.text)
                items = res[CountdownKeys.products.value][CountdownKeys.items.value]
                if len(items) == 0:
                    count += 1
                    print(f'{department["name"]}, {count} out of {len(departments)} DONE')
                    break
                for item in items:
                    if item[CountdownItemKeys.type.value] == CountdownItemIgnoreKeys.adds.value \
                            or CountdownItemKeys.price.value not in item:
                        continue
                    brand = item[CountdownItemKeys.brand.value]
                    if brand not in itemDict:
                        itemDict[brand] = []
                    name = item[CountdownItemKeys.name.value]
                    price = item[CountdownItemKeys.price.value][CountdownItemKeys.salePrice.value]
                    category = finalCategories.concatCategories(department[CountdownItemKeys.name.value])
                    photoUrl = item[CountdownItemKeys.images.value][CountdownItemKeys.iconLarge.value]
                    size = item[CountdownItemKeys.size.value][CountdownItemKeys.volumeSize.value]
                    if not size:
                        size = item[CountdownItemKeys.size.value][CountdownItemKeys.packageType.value]

                    if not item:
                        size = item[CountdownItemKeys.size.value][CountdownItemKeys.cupMeasure.value]
                    if not size:
                        size = item[CountdownItemKeys.unit.value]
                    parsedItem = {f'{OutputJsonKeys.name.value}': name,
                                  f'{OutputJsonKeys.price.value}': price,
                                  f'{OutputJsonKeys.category.value}': category,
                                  f'{OutputJsonKeys.photoUrl.value}': photoUrl,
                                  f'{OutputJsonKeys.size.value}': size,
                                  }
                    itemDict[brand].append(parsedItem)

        self._writeItem(itemDict, countDownDataFile, False)
        countDownDataFile.write("}\n")
        countDownDataFile.close()

    def _getFoodStuffsFacets(self, superMarket: SuperMarketAbbreviation, storeId) -> {str: int}:
        if superMarket == SuperMarketAbbreviation.packNSave:
            self._foodStuffsHeaders = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'PackNSaveApp/4.4.0 (iOS 16.3.1)',
                'Content-Length': '325',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Content-Type': 'application/json'
            }
        else:
            self._foodStuffsHeaders = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'NewWorldApp/4.4.0 (iOS 16.3.1)',
                'Content-Length': '325',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Content-Type': 'application/json'
            }

        requestBody = '{"query":"","facets":["category1NI","onPromotion"],"attributesToHighlight":[],' \
                      '"sortFacetValuesBy":"alpha","hitsPerPage":"1","facetFilters":[' \
                      f'"stores:{storeId}",' \
                      f'["onPromotion:{storeId}"],"tobacco:false"]' \
                      '}'
        url = f'https://api-prod.prod.fsniwaikato.kiwi' \
              f'/prod/mobile/v1/product/search/{superMarket.value}'
        headers = self._foodStuffsHeaders
        headers["Authorization"] = self._getToken(superMarketType=superMarket)
        response = requests.post(url, headers=self._foodStuffsHeaders, data=requestBody)
        dictionary = json.loads(response.text)
        dictionary = dictionary[FoodStuffsKeys.facets.value][FoodStuffsKeys.category1NI.value]
        facets = {}
        for k in dictionary.keys():
            v = dictionary[k]
            facets[k] = int(v)
        return facets

    def fetchFoodStuffsItems(self, superMarket: SuperMarketAbbreviation):
        url = "https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/store"
        if superMarket == SuperMarketAbbreviation.packNSave:
            self._foodStuffsHeaders = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'PackNSaveApp/4.5.0 (iOS 16.3.1)',
                'Accept-Language': 'en-GB,en;q=0.9'
            }
        else:
            self._foodStuffsHeaders = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'NewWorldApp/4.5.0 (iOS 16.3.1)',
                'Accept-Language': 'en-GB,en;q=0.9'
            }
        self._foodStuffsHeaders["Authorization"] = self._getToken(superMarketType=superMarket)
        req = requests.get(url, headers=self._foodStuffsHeaders)

        stores = json.loads(req.text)["stores"]
        storeIds = []
        for store in stores:
            storeIds.append(store["id"])
        parseDict = {}
        fileName = FileNames.newWorldFile.value
        if superMarket == SuperMarketAbbreviation.packNSave:
            fileName = FileNames.packNSaveFile.value
        outputFile = open(fileName, mode="w")
        storeIdsSize = len(storeIds)
        count = 1
        for identifier in storeIds:
            resDict = self._fetchFoodStuffIStoreItems(superMarket, identifier)
            for key in resDict.keys():
                if key not in parseDict.keys():
                    parseDict[key] = {}
                for item in resDict[key]:
                    name = item[OutputJsonKeys.name.value]
                    if name in parseDict[key].keys():
                        if identifier in parseDict[key][name][OutputJsonKeys.price.value].keys():
                            if float(item[OutputJsonKeys.price.value]) > float(parseDict[key][name][OutputJsonKeys.price.value][identifier]):
                                parseDict[key][name][OutputJsonKeys.price.value][identifier] = item[OutputJsonKeys.price.value]
                        else:
                            parseDict[key][name][OutputJsonKeys.price.value][identifier] = item[OutputJsonKeys.price.value]
                    else:
                        parsedItem = {}
                        parsedItem[OutputJsonKeys.name.value] = name
                        parsedItem[OutputJsonKeys.category.value] = item[OutputJsonKeys.category.value]
                        parsedItem[OutputJsonKeys.photoUrl.value] = item[OutputJsonKeys.photoUrl.value]
                        parsedItem[OutputJsonKeys.size.value] = item[OutputJsonKeys.size.value]
                        parsedItem[OutputJsonKeys.price.value] = {identifier: item[OutputJsonKeys.price.value]}
                        parseDict[key][name] = parsedItem
            print(f"done {count} out of {storeIdsSize}")
            count += 1
        itemsDict = {}
        for key in parseDict.keys():
            itemsDict[key] = []
            for item in parseDict[key].values():
                itemsDict[key].append(item)
        outputFile.write("{\n")
        self._writeItem(itemsDict, outputFile, True)
        outputFile.write("}\n")
        outputFile.close()

    def _fetchFoodStuffIStoreItems(self, superMarket: SuperMarketAbbreviation, storeId) -> dict:
        facets = self._getFoodStuffsFacets(superMarket, storeId)
        fcs = []
        count = 0
        threshold = 900
        st = ""
        for facet in facets.keys():
            value = facets[facet]
            if count + value >= threshold:
                st = st[:-1]
                fcs.append(st)
                count = 0
                st = ""
            count += value
            st += f'"{FoodStuffsKeys.category1NI.value}:{facet}",'

        if len(st) > 0:
            st = st[:-1]
            fcs.append(st)

        itemsDict = {}
        headers = self._foodStuffsHeaders

        for facet in fcs:
            requestBody = '{' + f'"query":"","facets":["{FoodStuffsKeys.category1NI.value}",' \
                                f'"onPromotion"],"attributesToHighlight":[],' \
                                '"sortFacetValuesBy":"alpha","hitsPerPage":"1000","facetFilters":[' \
                                f'"stores:{storeId}",' \
                                f'[{facet}],' \
                                f'["onPromotion:{storeId}"],"tobacco:false"]' \
                                '}'
            url = f'https://api-prod.prod.fsniwaikato.kiwi' \
                  f'/prod/mobile/v1/product/search/{superMarket.value}?sortOrder=popularity'
            headers["Authorization"] = self._token
            response = requests.post(url, headers=self._foodStuffsHeaders, data=requestBody)
            jsonResponse = json.loads(response.text)
            self._writeFoodStuffsResponse(itemsDict, jsonResponse, storeId)
        return itemsDict
    def _getToken(self, superMarketType: SuperMarketAbbreviation) -> str:
        headers = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'NewWorldApp/4.4.0 (iOS 16.3.1)',
                'Content-Length': '325',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Content-Type': 'application/json'
            }

        if superMarketType == SuperMarketAbbreviation.packNSave:
            headers = {
                'Host': 'api-prod.prod.fsniwaikato.kiwi',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'PackNSaveApp/4.4.0 (iOS 16.3.1)',
                'Content-Length': '325',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Content-Type': 'application/json'
            }

        try:
            refreshTokenFile = open(f"{superMarketType.value}refreshToken.txt", mode="r")
            url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/users/login/refreshtoken'
            refreshToken = refreshTokenFile.readline(1)
            body = f'"refreshToken":"{refreshToken}"'
            body = "{" + body + "}"
            response = requests.post(url, headers=headers, data=body)
            responseJson = json.loads(response.text)
            bearerToken = responseJson[FoodStuffsKeys.accessToken.value]
            newRefreshToken = responseJson[FoodStuffsKeys.refreshToken.value]
            refreshTokenFile.close()
            refreshTokenFile = open(f"{superMarketType.value}refreshToken.txt", mode="w")
            refreshTokenFile.write(newRefreshToken)
            refreshTokenFile.close()
            self._token = f'Bearer {bearerToken}'
            return f'Bearer {bearerToken}'
        except:
            # log in
            url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/user/login'
            body = '{' + \
                   f'"email":"{os.getenv("EMAIL")}",' \
                   f'"password":"{os.getenv("EMAIL_PASSWORD")}",' \
                   f'"banner":"{superMarketType.value}"' + \
                   '}'
            response = requests.post(url, headers=headers, data=body)
            responseJson = json.loads(response.text)
            bearerToken = responseJson[FoodStuffsKeys.access_token.value]
            newRefreshToken = responseJson[FoodStuffsKeys.refresh_token.value]
            refreshTokenFile = open(f"{superMarketType.value}refreshToken.txt", mode="w")
            refreshTokenFile.write(newRefreshToken)
            refreshTokenFile.close()
            self._token = f'Bearer {bearerToken}'
            return f'Bearer {bearerToken}'

    def _writeItem(self, dictionary, file, hasMultiplePrices):
        numBrands = len(dictionary.keys()) - 1
        siz = []
        for brandIndex, brand in enumerate(dictionary.keys()):
            file.write(f'    "{brand}": [\n')
            numItems = len(dictionary[brand]) - 1
            for itemIndex, item in enumerate(dictionary[brand]):
                name = item[OutputJsonKeys.name.value]
                price = item[CountdownItemKeys.price.value]
                priceStrig = f'"{price}"'
                if hasMultiplePrices:
                    priceStrig = "{"
                    for priceKey in price.keys():
                        priceStrig += f'"{priceKey}": "{price[priceKey]}",'
                    priceStrig = priceStrig[:-1]
                    priceStrig += "}"
                category = item[OutputJsonKeys.category.value]
                photoUrl = item[OutputJsonKeys.photoUrl.value]
                name = name.replace(f'-{item[OutputJsonKeys.size.value]}', "").replace('"', "")
                numbers = re.findall(r'[0-9]+[aA-zZ]?[ ]+', name)
                for number in numbers:
                    name = name.replace(number, "")
                size = self._parseSize(item[OutputJsonKeys.size.value])
                if size not in siz:
                    siz.append(size)
                if numItems == itemIndex:
                    file.write(
                        '        { ' +
                        f'"{OutputJsonKeys.name.value}": "{name}", ' +
                        f'"{CountdownItemKeys.price.value}": {priceStrig}, ' +
                        f'"{OutputJsonKeys.category.value}": "{category}",' +
                        f'"{OutputJsonKeys.photoUrl.value}": "{photoUrl}",' +
                        f'"{OutputJsonKeys.size.value}": "{size}"' +
                        '}\n')
                else:
                    file.write(
                        '        { ' +
                        f'"{OutputJsonKeys.name.value}": "{name}", '
                        + f'"{CountdownItemKeys.price.value}": {priceStrig}, ' +
                        f'"{OutputJsonKeys.category.value}": "{category}",' +
                        f'"{OutputJsonKeys.photoUrl.value}": "{photoUrl}",' +
                        f'"{OutputJsonKeys.size.value}": "{size}"' +
                        '},\n')

            if brandIndex == numBrands:
                file.write("    ]\n")
            else:
                file.write("    ],\n")

    def _parseSize(self, size: str) -> str:
        cleanUpDict = {
            "per ": "1 ",
            "medium": "",
            "small": "",
            "large": "",
            "tray": "",
            "pk": "pack ",
            "ea ": "each "
        }
        if size[-2:] == "ea":
            size = size[:-2]
            size += "each"
        size = size.lower()
        packs = re.findall(r'[x ]+[0-9]+[aA-zZ]+', size)
        for pack in packs:
            size = size.replace(pack, "pack")
        for key in cleanUpDict.keys():
            size = size.replace(key, cleanUpDict[key])
        return size

    def _writeFoodStuffsResponse(self, itemsDict, jsonResponse: {str: typing.Any}, storeId: str):
        items = jsonResponse[FoodStuffsKeys.products.value]
        storeId = storeId.replace("-", "")
        for item in items:
            price = 1
            if storeId in item[FoodStuffsItemKeys.price.value].keys():
                price = item[FoodStuffsItemKeys.price.value][storeId]
            brand = "supermarket brand"
            if FoodStuffsItemKeys.brand.value in item.keys():
                brand = item[FoodStuffsItemKeys.brand.value]
            brand = brand.replace('"', "")
            if brand not in itemsDict:
                itemsDict[brand] = []

            name = item[FoodStuffsItemKeys.name.value].replace('"', "")
            price = price
            category = finalCategories.concatCategories(item[FoodStuffsItemKeys.category.value][0])
            objectId = item[FoodStuffsItemKeys.objectID.value].split("-")[0]
            photoUrl = f'https://a.fsimg.co.nz/product/retail/fan/image/200x200/{objectId}.png'
            size = "each"
            if FoodStuffsItemKeys.size.value in item.keys():
                size = item[FoodStuffsItemKeys.size.value]
            name = name + "-" + size
            parsedItem = {
                f'{OutputJsonKeys.name.value}': name,
                f'{OutputJsonKeys.price.value}': price,
                f'{OutputJsonKeys.category.value}': category,
                f'{OutputJsonKeys.photoUrl.value}': photoUrl,
                f'{OutputJsonKeys.size.value}': size
            }
            itemsDict[brand].append(parsedItem)