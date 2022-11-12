import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

import pandas as pd

from hotels.models import Hotel
from main.models import Region, DetailRegion

# 기존 엑셀 파일 불러오기
df = pd.read_excel('hotel_list.xlsx', engine='openpyxl')

for i in range(200):
    new_hotel = Hotel(
    region=Region.objects.get(name=df['region'][i]),
    detail_region=DetailRegion.objects.get(name=df['detail_region'][i]),
    name=df['name'][i],
    url=df['url'][i],
    rating=df['rating'][i],
    grade=df['grade'][i],
    price=df['price'][i],
    address=df['address'][i],
    facilities=df['facilities'][i],
    image=df['image'][i],
    )
    new_hotel.save()