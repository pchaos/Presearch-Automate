# -*- coding: utf-8 -*- #
import os, sys
import json
import time
import random
from selenium import webdriver
import pickle
from dotenv import load_dotenv

# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

email=os.getenv("EMAIL")
password=os.getenv("PASSWORD")
searchcounts=int(os.getenv("SEARCHCOUNTS"))  # 查询次数
headless=bool(int(os.getenv("HEADLESS")))
if headless:
    print("headless mode")
cookieFileName = 'presearch.cookies.pkl'
PROXY = "127.0.0.1:1080"  #  HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = headless 
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument("ignore-certificate-errors")
chrome_options.add_argument("--window-size=1280,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.ipchicken.com/")
if os.path.exists(cookieFileName):
    #  url = 'https://www.presearch.org/'
    cookies = pickle.load(open(cookieFileName, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
else:
    pass

url = 'https://www.presearch.org/login'
driver.get(url)
#  headers = {'User-Agent': 'Chrome/69.0.3396.09'}

filePath = 'MaleNameData.json'  # Path of json
nameList = []
with open(filePath) as file:
    data = json.load(file)
for i in range(len(data)):
    nameList.append(random.choice(data))
    #  nameList.append(data[i]['Male'])
#  print(nameList)

try:
    driver.find_element_by_name('email').send_keys(email)  # enter your email
    driver.find_element_by_name('password').send_keys(password)  # enter your password
    time.sleep(1.5)
    seq = driver.find_element_by_tag_name('iframe')
    # frames
    fr = driver.find_elements_by_tag_name('iframe')
    if seq:
        driver.switch_to.frame(seq)
        # click recaptcha
        driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]').click()
        time.sleep(2)
        #  driver.implicitly_wait(15)
        driver.switch_to.default_content()
    
    if os.path.exists(cookieFileName):
        # 重新登录系统，删除以前的cookie文件
        os.remove(cookieFileName)
except Exception as e:
    url = 'https://www.presearch.org/login'
    print("using cookies, no need login")

# waiting login in
counts = 200
print("waiting ", end='')
for i in range(counts):
    time.sleep(2)
    if driver.current_url != url:
        print(driver.current_url)
        driver.switch_to.default_content()
        break
    print(".", end='', flush=True)

if not os.path.exists(cookieFileName):
    # 保存cookies，下次免登录
    pickle.dump(driver.get_cookies(), open(cookieFileName, "wb"))

#  for i in nameList[:40]:
for i in nameList[:searchcounts]:
    time.sleep(2)
    driver.find_element_by_id('search').send_keys(i['Male'])
    driver.find_element_by_xpath(
        '//*[@id="search-input"]/div/span/button').click()
    time.sleep(5)
    driver.get(url)
    print("$", end='', flush=True)

driver.close()
