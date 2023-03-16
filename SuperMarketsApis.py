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

    _newWorldHeaders = {
        'Host': 'api-prod.prod.fsniwaikato.kiwi',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'NewWorldApp/4.4.0 (iOS 16.3.1)'
    }

    newWordHeaders2 = {
        'Host': 'api-prod.prod.fsniwaikato.kiwi',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'NewWorldApp/4.4.0 (iOS 16.3.1)',
        'Content-Length': '325',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Content-Type': 'application/json'
    }

    nwBody = '{"query":"","facets":["category1NI","DisplayName","onPromotion"],"attributesToHighlight":[],"sortFacetValuesBy":"alpha","maxValuesPerFacet":"1000","hitsPerPage":"100","facetFilters":["stores:63cbb6c6-4a0b-448d-aa78-8046692a082c",["onPromotion:63cbb6c6-4a0b-448d-aa78-8046692a082c"],"tobacco:false"]}'

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
    def fetchNewworldItems(self):
        #lastPage = self._getCountdownLastPage()
        #url = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/promos?storeId=63cbb6c6-4a0b-448d-aa78-8046692a082c&products=5023660-EA-000%2C5010717-EA-000%2C5103401-KGM-000%2C5010719-EA-000%2C5009708-EA-000%2C5010716-EA-000%2C5003157-EA-000%2C5034758-EA-000%2C5009651-EA-000%2C5002738-EA-000%2C5014564-EA-000%2C5001903-EA-000%2C5010720-EA-000%2C5019940-EA-000%2C5014563-EA-000%2C5007378-EA-000%2C5003623-EA-000%2C5009951-EA-000%2C5034760-EA-000%2C5001769-EA-000%2C5009952-EA-000%2C5011412-EA-000%2C5100303-KGM-000%2C5013751-EA-000%2C5004416-EA-000%2C5001313-EA-000%2C5009950-EA-000%2C5010721-EA-000%2C5034757-EA-000%2C5230700-EA-000%2C5004423-EA-000%2C5007555-EA-000%2C5025925-EA-000%2C5034759-EA-000%2C5264171-EA-000%2C5249650-EA-000%2C5007494-EA-000%2C5011410-EA-000%2C5005217-EA-000%2C5016928-EA-000%2C5010410-EA-000%2C5035008-EA-000%2C5010699-EA-000%2C5032122-EA-000%2C5264173-EA-000%2C5003627-EA-000%2C5215070-EA-000%2C5001900-EA-000%2C5009655-EA-000%2C5030647-EA-000%2C5217244-EA-000%2C5030846-EA-000%2C5001361-EA-000%2C5003276-EA-000%2C5013073-EA-000%2C5230685-EA-000%2C5027950-EA-000%2C5027137-EA-000%2C5027140-EA-000%2C5026161-EA-000%2C5249645-EA-000%2C5015656-EA-000%2C5249654-EA-000%2C5014501-EA-000%2C5015760-EA-000%2C5010718-EA-000%2C5010411-EA-000%2C5002415-EA-000%2C5009494-EA-000%2C5103890-KGM-000%2C5002412-EA-000%2C5005255-EA-000%2C5256569-EA-000%2C5011693-EA-000%2C5002084-EA-000%2C5005605-EA-000%2C5042043-EA-000%2C5011153-EA-000%2C5010481-EA-000%2C5007407-EA-000%2C5001801-EA-000%2C5017804-EA-000%2C5017417-EA-000%2C5010413-EA-000%2C5007316-EA-000%2C5016213-EA-000%2C5004556-EA-000%2C5005705-EA-000%2C5011411-EA-000%2C5000560-EA-000%2C5025999-EA-000%2C5004703-EA-000%2C5009650-EA-000%2C5019937-EA-000%2C5004670-EA-000%2C5217171-EA-000%2C5020541-EA-000%2C5004739-EA-000%2C5234250-EA-000%2C5274512-EA-000'
        #response = requests.get(url, headers=self._newWorldHeaders)
        url1 = 'https://api-prod.prod.fsniwaikato.kiwi/prod/mobile/v1/product/search/MNW?sortOrder=popularity'
        res2 = requests.post(url1, headers=self.newWordHeaders2, data=self.nwBody)
        # res = json.loads(response.text)
        print(res2.text)
    def _getCountdownLastPage(self) -> int:
        maxSupoortedPages = 300
        response = requests.get(f'https://www.countdown.co.nz/api/v1/products?target=specials&page={maxSupoortedPages}',
                         headers = self._countDownHeaders)
        extracted = re.findall(r'and [0-9]+', response.text)
        if len(extracted) > 0:
            number = str(extracted[0]).strip("and ")
            return int(number)

        return maxSupoortedPages
