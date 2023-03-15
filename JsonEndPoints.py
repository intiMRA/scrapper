import requests
countDownHeaders = {
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
x = requests.get('https://www.countdown.co.nz/api/v1/products?target=specials&page=10', headers=countDownHeaders)
print(x.text)

