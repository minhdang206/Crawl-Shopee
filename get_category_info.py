# Import các thư viện và package cần thiết
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml
import bs4
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime
from IPython.display import clear_output
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException

def click_ele(ele,time_sleep):
  action = ActionChains(driver)
  action.move_to_element(ele).perform()
  ele.click()
  sleep(time_sleep)
def scroll_element(element,amount=None):
  if amount:
    scroll_origin = ScrollOrigin.from_element(element)
    ActionChains(driver)\
      .scroll_from_origin(scroll_origin, 0, amount)\
      .perform()
  else:
    ActionChains(driver)\
      .scroll_to_element(element)\
      .perform()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("no-sandbox")
options.add_argument("window-size=1280,800")
options.add_experimental_option("prefs",{"credentials_enable_service": False,
                                        "profile.password_manager_enabled": False,
                                        "profile.default_content_setting_values.notifications" : 2,
                                        "useAutomationExtension" :False})
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()), options=options)
service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Chrome(excutable_path=PATH_CHROME_BETA, options=options)

driver.get('https://shopee.vn/')
sleep(2)

shadow_root = driver.find_elements(By.CSS_SELECTOR, f'shopee-banner-popup-stateful')[0].shadow_root
btn_popup = shadow_root.find_elements(By.CSS_SELECTOR, f'div[class="shopee-popup__close-btn"]')
if btn_popup != []:
  click_ele(btn_popup[0], time_sleep=0.3)

list_category = driver.find_elements(By.CSS_SELECTOR, f'a[class="home-category-list__category-grid"]')
scroll_element(list_category[0], amount=250)

list_category = driver.find_elements(By.CSS_SELECTOR, f'a[class="home-category-list__category-grid"]')
set_cats_info = []

for cat in list_category:
  if cat.text:
    set_cats_info.append((cat.text, cat.get_attribute("href")))
print(set_cats_info)
# Kiểm tra lướt hết danh mục
div_category_carousel = driver.find_elements(By.CSS_SELECTOR, f'div[class="shopee-header-section home-category-list__header shopee-header-section--simple"]')[0]
arrow_next_btn = div_category_carousel.find_elements(By.CSS_SELECTOR, f'div[class^="carousel-arrow carousel-arrow--next"][style*="visible"]')

if arrow_next_btn != []:
  next_slide = True
else:
  next_slide = False
while next_slide:
  click_ele(arrow_next_btn[0], time_sleep=1)
  sleep(1.5)
  list_category = driver.find_elements(By.CSS_SELECTOR, f'a[class="home-category-list__category-grid"]')
  for cat in list_category:
    if cat.text:
      set_cats_info.append((cat.text, cat.get_attribute("href")))
  arrow_next_btn = div_category_carousel.find_elements(By.CSS_SELECTOR, f'div[class^="carousel-arrow carousel-arrow--next"][style*="visible"]')
  if arrow_next_btn != []:
    next_slide = True
  else:
    next_slide = False
print(set_cats_info)

set_category = set(set_cats_info)
print(f"Get done {len(set_category)} categories")

df_cat = pd.DataFrame(set_category, columns=['category', 'category_url'])
df_cat.to_csv('category_info.csv', index=False)
print(f"Saved to csv")
# driver.close()