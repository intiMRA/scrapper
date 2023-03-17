from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
driver = webdriver.Chrome(ChromeDriverManager().install())
newWorldId = "60928d93-06fa-4d8f-92a6-8c359e7e846d"
pakNSaveId = "e1925ea7-01bc-4358-ae7c-c6502da5ab12"
countdownUrlCall = "https://www.countdown.co.nz/shop/browse/departments"
newWorldUrlCall = f'https://www.newworld.co.nz/CommonApi/Navigation/MegaMenu?v=&storeId={newWorldId}'
pakNSavwUrlCall = f'https://www.paknsave.co.nz/CommonApi/Navigation/MegaMenu?v=&storeId={pakNSaveId}'
urlRegex = r"/shop/[aA-zZ/0-9?\-=]+"
endpoints = open("endpoints.txt", mode="w")
endpoints.write("[\n")
driver.get(countdownUrlCall)
time.sleep(3)
cdown = re.findall(urlRegex, driver.page_source)

driver.get(newWorldUrlCall)
time.sleep(3)
nworld = re.findall(urlRegex, driver.page_source)

driver.get(pakNSavwUrlCall)
time.sleep(3)
psave = re.findall(urlRegex, driver.page_source)

for c in cdown:
    endpoints.write(f"    \"https://www.countdown.co.nz{c}\",\n")
for nw in nworld:
    endpoints.write(f"    \"https://www.newworld.co.nz{nw}\",\n")
for ps in psave:
    endpoints.write(f"    \"https://www.paknsave.co.nz{ps}\",\n")
endpoints.write("]")
endpoints.close()
driver.close()
