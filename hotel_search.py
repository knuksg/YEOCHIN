import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# 검색어 설정
resion = 'Busan_Province'
url = 'https://hotels.naver.com/list?placeFileName=place%3A' + resion + '&adultCnt=2&checkIn=2022-11-16&checkOut=2022-11-17&sortField=popularityKR&sortDirection=descending'

# 크롬 구동
driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
driver.get(url)
time.sleep(2)

# 호텔 이름/링크 찾기
hotel_name_list = driver.find_elements(By.CSS_SELECTOR, '.Detail_title__40_dz')[:1]
hotel_url_list = driver.find_elements(By.CSS_SELECTOR, '.SearchList_anchor__rKpmX')[:1]
hotel_image_list = []
hotel_rating_list = []
hotel_grade_list = []
hotel_price_list = []
hotel_address_list = []
hotel_facilities_list = []

# for문으로 개별 값 넣어주기.
for i in range(len(hotel_name_list)):
    hotel_name_list[i] = hotel_name_list[i].text
    hotel_url_list[i] = hotel_url_list[i].get_attribute('href')

    driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
    driver.get(hotel_url_list[i])
    time.sleep(3)

    hotel_image_list.append(driver.find_element(By.CSS_SELECTOR, '.ThumbnailImage_img__yRn_t').get_attribute('src'))
    hotel_rating_list.append(driver.find_element(By.CSS_SELECTOR, '.common_score__kI5HY').text)
    hotel_grade_list.append(driver.find_element(By.CSS_SELECTOR, '.common_grade__FS6L0').text)
    hotel_price_list.append(driver.find_element(By.CSS_SELECTOR, '.common_price__mpQkf').text)
    hotel_address_list.append(driver.find_element(By.CSS_SELECTOR, '.Address_txt__O_b0B').text)
    facilities_list = driver.find_elements(By.CSS_SELECTOR, '.Facilities_facility__ByaZY')
    facilities_str = []
    for facilities in facilities_list:
        facilities_class = facilities.get_attribute('class')
        facilities_str.append(facilities_class[41:-1])
    hotel_facilities_list.append(facilities_str)

# 데이터프레임으로 만들기
df = pd.DataFrame({
    'name': hotel_name_list, 
    'url': hotel_url_list,
    'rating': hotel_rating_list,
    'grade': hotel_grade_list,
    'price': hotel_price_list,
    'address': hotel_address_list,
    'facilities': hotel_facilities_list,
    'image': hotel_image_list,
    })

# 엑셀로 저장하기
df.to_excel('busan_hotel_list.xlsx', encoding='utf-8-sig')

