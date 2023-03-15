from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import requests
from Database import Database

# driver = webdriver.Chrome(ChromeDriverManager().install())
# countdownUrlCall = "https://www.countdown.co.nz/shop/browse/departments"
# newWorldUrlCall = "https://www.newworld.co.nz/CommonApi/Navigation/MegaMenu?v=&storeId=60928d93-06fa-4d8f-92a6-8c359e7e846d"
# pakNSavwUrlCall = "https://www.paknsave.co.nz/CommonApi/Navigation/MegaMenu?v=&storeId=e1925ea7-01bc-4358-ae7c-c6502da5ab12"
# urlRegex = r"/shop/[aA-zZ/0-9?\-=]+"
# driver.get(countdownUrlCall)
# time.sleep(3)
# cdown = re.findall(urlRegex, driver.page_source)
#
# driver.get(newWorldUrlCall)
# time.sleep(3)
# nw = re.findall(urlRegex, driver.page_source)
#
# driver.get(pakNSavwUrlCall)
# time.sleep(3)
# ps = re.findall(urlRegex, driver.page_source)
#
# print(cdown)
# print(nw)
# print(ps)

# r1 = r';name=[aA-zZ\-0-9\']+'
# r2 = r'\$[0-9]+[.]+[0-9]+'
# s = re.findall(rf'{r1}|{r2}', driver.page_source)
# print(s)
# for url in urls:
#     if "https" in url or "http" in url:
#         continue
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     surl = re.findall(r'/.*', url)[0]
#     driver.get(f'https://www.newworld.co.nz{surl}')
#     time.sleep(3)
#     s = driver.page_source
#     productName = "&quot;productName&quot;.*&quot"
#     pricePerItem = "&quot;PricePerItem&quot;.*&quot"
#     r = re.findall(rf'{productName}|{pricePerItem}', s)
#     print(surl)
#     print("-"*50)
#     for w in r:
#         print(str(w).replace("&quot", "").replace(";", ""))
#     driver.close()

# driver.get("https://www.countdown.co.nz/shop/browse/departments")
# time.sleep(10)
# print(driver.page_source)
# driver.close()

db = Database()
db.startConnection()
db.testConnection()
db.createTable(tableName="NewWorld", tablePatameters=["itemName VARCHAR(255)", "itemPrice VARCHAR(255)"])
db.printTables()
db.closeConnection()