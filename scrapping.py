from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
import requests

prov = str(input('Provinsi : '))
kab = str(input('Kota/Kab : '))
kec = str(input('kecamatan : '))


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
        print(f"Gagal Donwload Gambar: {url}")

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)
driver.get('https://pemilu2024.kpu.go.id/pilpres/hitung-suara')
driver.maximize_window()
sleep(3)

provinsi=driver.find_element(By.XPATH,"""/html/body/div/div[1]/div/div[1]/div/div/div/div[1]/div[3]/div/div/div[1]/input""")
provinsi.clear()
provinsi.send_keys(prov)
provinsi.send_keys(Keys.ENTER)
sleep(3)

kabupaten=driver.find_element(By.XPATH,"""//*[@id="vs8__combobox"]/div[1]/input""")
kabupaten.clear()
kabupaten.send_keys(kab)
kabupaten.send_keys(Keys.ENTER)
sleep(3)

kecamatan=driver.find_element(By.XPATH,"""//*[@id="vs13__combobox"]/div[1]/input""")
kecamatan.clear()
# kecamatan.send_keys('Banua Lawas')
kecamatan.send_keys(kec)
kecamatan.send_keys(Keys.ENTER)
sleep(3)


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

    print(f"{len(tps_url)} TPS")

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
    
    

driver.close()