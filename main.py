from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.newworld.co.nz/CommonApi/Navigation/MegaMenu?v=&storeId=60928d93-06fa-4d8f-92a6-8c359e7e846d")
urls = re.findall(r"URL\"[ ]*:[ ]*\"[aA-zZ/0-9?\-=]+", driver.page_source)
for url in urls:
    if "https" in url or "http" in url:
        continue
    driver = webdriver.Chrome(ChromeDriverManager().install())
    surl = re.findall(r'/.*', url)[0]
    driver.get(f'https://www.newworld.co.nz{surl}')
    time.sleep(3)
    s = driver.page_source
    productName = "&quot;productName&quot;.*&quot"
    pricePerItem = "&quot;PricePerItem&quot;.*&quot"
    r = re.findall(rf'{productName}|{pricePerItem}', s)
    print(surl)
    print("-"*50)
    for w in r:
        print(str(w).replace("&quot", "").replace(";", ""))
    driver.close()
driver.close()

