import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

import pandas as pd

from hotels.models import Hotel
from main.models import Region, DetailRegion

def create_region():
    # region & detail_region 생성하기
    resions_list = [
        ['서울', ['서울']],
        ['제주도', ['제주도']],
        ['인천', ['인천']],
        ['부산', ['부산']],
        ['경상도', ['대구', '경주']],
        ['경기도', ['가평']],
        ['강원도', ['강릉']],
        ['전라도', ['전주']],
        ['충청도', ['대전']]
        ]
    for regions in resions_list:
        Region.objects.create(name=regions[0])
        model_region = Region.objects.get(name=regions[0])
        for region in regions[1]:
            DetailRegion.objects.create(region=model_region, name=region)
def hotel_add():
    # 기존 엑셀 파일 불러오기
    df = pd.read_excel("hotel_list.xlsx", engine="openpyxl")

    for i in range(200):
        new_hotel = Hotel(
            region=Region.objects.get(name=df["region"][i]),
            detail_region=DetailRegion.objects.get(name=df["detail_region"][i]),
            name=df["name"][i],
            url=df["url"][i],
            rating=df["rating"][i],
            grade=df["grade"][i],
            price=df["price"][i],
            address=df["address"][i],
            facilities=df["facilities"][i],
            image=df["image"][i],
        )
        new_hotel.save()

def run():
    create_region()
    # 호텔 추가시 지역 생성 함수는 주석 처리할 것!
    hotel_add()