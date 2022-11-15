import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

resion_list = [
    'Daegu_Metropolitan_City', 'Busan_Province', 
    'Seoul', 'Jeju_Province', 
    'Incheon_Metropolitan_City', 'Jeonju',
    'Gangneung', 'Daejeon_Metropolitan_City',
    'Gapyeong', 'Gyeongju',
    ]

# 검색어 설정
resion = 'Gyeongju'
url = 'https://hotels.naver.com/list?placeFileName=place%3A' + resion + '&adultCnt=2&checkIn=2022-11-16&checkOut=2022-11-17&sortField=popularityKR&sortDirection=descending'
resion = '경상도'
detail_resion = '경주'

# 크롬 구동
driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
driver.get(url)
time.sleep(2)

# 호텔 이름/링크 찾기
hotel_region_list = []
hotel_detail_region_list = []
hotel_name_list = driver.find_elements(By.CSS_SELECTOR, '.Detail_title__40_dz')
hotel_url_list = driver.find_elements(By.CSS_SELECTOR, '.SearchList_anchor__rKpmX')
hotel_image_list = []
hotel_rating_list = []
hotel_grade_list = []
hotel_price_list = []
hotel_address_list = []
hotel_facilities_list = []

# for문으로 개별 값 넣어주기.
for i in range(len(hotel_name_list)):
    try:
        hotel_region_list.append(resion)
        hotel_detail_region_list.append(detail_resion)
        hotel_name_list[i] = hotel_name_list[i].text
        hotel_url_list[i] = hotel_url_list[i].get_attribute('href')

        driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
        driver.get(hotel_url_list[i])
        time.sleep(5)

        print(i)

        hotel_image_list.append(driver.find_element(By.CSS_SELECTOR, '.ThumbnailImage_img__yRn_t').get_attribute('src'))
        hotel_rating = driver.find_element(By.CSS_SELECTOR, '.common_score__kI5HY').text
        if hotel_rating.isdisit():
            hotel_rating_list.append(hotel_rating)
        else:
            hotel_rating_list.append(0)
        try:
            hotel_grade_list.append(driver.find_element(By.CSS_SELECTOR, '.common_grade__FS6L0').text)
        except:
            hotel_grade_list.append('등급없음')
        hotel_price_list.append(driver.find_element(By.CSS_SELECTOR, '.common_price__mpQkf').text.rstrip('원'))
        hotel_address_list.append(driver.find_element(By.CSS_SELECTOR, '.Address_txt__O_b0B').text)
        facilities_list = driver.find_elements(By.CSS_SELECTOR, '.Facilities_facility__ByaZY')
        facilities_str = []
        for facilities in facilities_list:
            facilities_class = facilities.get_attribute('class')
            facilities_str.append(facilities_class[41:-1])
        hotel_facilities_list.append(facilities_str)
    except:
        hotel_name_list[i] = '오류'
        hotel_url_list[i] = '오류'
        continue

# 오류 제거
while '오류' in hotel_name_list or '오류' in hotel_url_list:
    hotel_name_list.remove('오류')
    hotel_url_list.remove('오류')

# 데이터프레임으로 만들기
new_df = pd.DataFrame({
    'region': hotel_region_list,
    'detail_region': hotel_detail_region_list,
    'name': hotel_name_list, 
    'url': hotel_url_list,
    'rating': hotel_rating_list,
    'grade': hotel_grade_list,
    'price': hotel_price_list,
    'address': hotel_address_list,
    'facilities': hotel_facilities_list,
    'image': hotel_image_list,
    })
print(new_df)

# 기존 데이터프레임 불러오기
df = pd.read_excel('hotel_list.xlsx', engine='openpyxl')
print(df)

# 기존 데이터프레임과 합치기
df = pd.concat([df, new_df], ignore_index=True)

# 엑셀로 저장하기
df.to_excel('hotel_list.xlsx', index=False, encoding='utf-8-sig')

