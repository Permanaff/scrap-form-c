#you tube comments on  you tube orignal Ai series.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
from datetime import datetime
import os
import time
import requests

OUTPUT_DIR = "Formulir_C"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download image: {url}")

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)
driver.get('https://pemilu2024.kpu.go.id/pilpres/hitung-suara')
driver.maximize_window()
sleep(3)

provinsi=driver.find_element(By.XPATH,"""/html/body/div/div[1]/div/div[1]/div/div/div/div[1]/div[3]/div/div/div[1]/input""")
provinsi.clear()
provinsi.send_keys('Kalimantan Selatan')
provinsi.send_keys(Keys.ENTER)
sleep(3)

kabupaten=driver.find_element(By.XPATH,"""//*[@id="vs8__combobox"]/div[1]/input""")
kabupaten.clear()
kabupaten.send_keys('Tabalong')
kabupaten.send_keys(Keys.ENTER)
sleep(3)

kabupaten=driver.find_element(By.XPATH,"""//*[@id="vs13__combobox"]/div[1]/input""")
kabupaten.clear()
# kabupaten.send_keys('Banua Lawas')
kabupaten.send_keys('Bintang Ara')
kabupaten.send_keys(Keys.ENTER)
sleep(3)

# district = driver.find_element(By.LINK_TEXT, 'Banua Lawas')
# district.click()
# sleep(2)

kelurahan_link = driver.find_elements(By.CSS_SELECTOR, "a[href*='/pilpres/hitung-suara/']")
kelurahan_url = [link.get_attribute("href") for link in kelurahan_link]
print(kelurahan_url)
print(f"{len(kelurahan_url)} Kelurahan")
kelurahan_url = kelurahan_url[2:]
# sleep(50)
sleep(3)

for kelurahan in kelurahan_url :
    driver.get(kelurahan)
    sleep(2)

    tps_link = driver.find_elements(By.CSS_SELECTOR, "a[href*='/pilpres/hitung-suara/']")
    tps_url = [link.get_attribute("href") for link in tps_link]
    tps_url = tps_url[3:]
    sleep(2)

    for tps in tps_url :
        driver.get(tps)
        sleep(2)

        tps_number = tps.split("/")[-1]

        try : 
            images=driver.find_element(By.XPATH,"""//*[@id="main"]/div[3]/div[2]/div[2]/div[3]/div[2]/div/div[2]/a/img""")
            image_src = images.get_attribute("src")
        except Exception as e : 
            pass

        download_image(image_src, f"A_{tps_number}.jpg")

        # sleep(2)
    
    print(f"{len(tps_url)} TPS")
    # for x in tps_urls :
    #     print(x)

    # for tps in tps_urls :
    #     driver.get(tps)
    #     sleep(2)




# for i in range(8):
#     driver.execute_script("window.scrollBy(0,700)","")
#     sleep(2)
# sleep(5)
# container_element = driver.find_element(By.CLASS_NAME,'css\\-rjanld')
# driver.execute_script("arguments[0].scrollIntoView();", container_element)


# pagination = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, './/*[@id="zeus-root"]/div/div[2]/div/div[2]/div[5]/nav'))
# )
# pages = pagination.find_element(By.XPATH, './/ul[contains(@class, "css-1ni9y5x-unf-pagination-items")]')
# page_items = pages.find_elements(By.TAG_NAME, 'li')
# last_page = int(page_items[-2].text.replace('.', ''))
# if last_page >= 10 : 
#     last_page = 10

# # sleep(10)
# title_product = []
# product_price = []
# seller_product = []
# product_sell = []
# product_image = []
# current_page = 1


# while current_page <= last_page:
#     sleep(5)
#     products = driver.find_elements(By.CLASS_NAME, "css-5wh65g")

#     for product in products:
#         try : 
#             title = product.find_element(By.CLASS_NAME, 'OWkG6oHwAppMn1hIBsC3pQ\\=\\=').text
#         except NoSuchElementException:
#             title = None

#         try : 
#             title = title.replace(",", " ")
#         except NoSuchElementException:
#             title = title
#         title_product.append(title)

#         try:
#             price = product.find_element(By.CLASS_NAME, '_8cR53N0JqdRc\\+mQCckhS0g\\=\\=').text
#         except NoSuchElementException:
#             try:
#                 price = product.find_element(By.CLASS_NAME, 'gJHohDcsji\\+TjH4Kkc9LEw\\=\\=').text
#             except NoSuchElementException:
#                 price = None
#         product_price.append(price)

        
#         try:
#             # Mencoba menemukan elemen pertama
#             sell = product.find_element(By.CLASS_NAME, 'eLOomHl6J3IWAcdRU8M08A\\=\\=').text
#         except NoSuchElementException:
#             sell = None

#         product_sell.append(sell)

#         try:
#             image = product.find_element(By.CLASS_NAME, 'css\\-1c345mg').get_attribute('src')
#         except NoSuchElementException:
#             image = None
#         product_image.append(image)

#         try:
#             seller = product.find_element(By.CLASS_NAME, 'X6c\\-fdwuofj6zGvLKVUaNQ\\=\\=').text

#             if seller == 'Dilayani Tokopedia' : 
#                 try:
#                     seller = product.find_element(By.XPATH, '//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[4]/div[1]/div[8]/a/div[1]/div[2]/div[4]/div[2]/span[2]').get_attribute('src')
#                 except NoSuchElementException:
#                     seller = None

#         except NoSuchElementException:
#             seller = None

#         seller_product.append(seller)

        
#         print(f"{title}\n{price}\n{sell}\n{image}\n--------------------")

#         try : 
#             escaped_title = title.replace("'", "\\'").replace('"', '\\"')
#         except NoSuchElementException:
#             escaped_title = title

#         # if "'" in title or '"' in title:
#         #     escaped_title = title.replace("'", "\\'").replace('"', '\\"')
        
#         driver.execute_script(f'console.log(`{escaped_title}`);')

#     driver.execute_script(f'console.log(">>>>> Data Terambil :  {len(title_product)} <<<<<");')
#     current_page = current_page + 1
#     try:
#         next_page = driver.find_element(By.XPATH, './/button[contains(@class, "css-16uzo3v-unf-pagination-item")][@aria-label="Laman berikutnya"]')
#         if next_page.is_enabled():
#             next_page.click()
#             driver.execute_script(f'console.log(">>>>> HALAMAN {current_page} <<<<<");')
#         else:
#             break
#     except NoSuchElementException:
#         break


# time = datetime.now().strftime("%y%m%d%H%M%S")

# df=pd.DataFrame({"title":title_product, 'harga' : product_price, 'terjual' : product_sell, 'seller' : seller_product})
# df.to_csv(f"product_{time}.csv",index=False)
# assert "No results found." not in driver.page_source
driver.close()