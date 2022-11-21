from django.shortcuts import render, get_object_or_404
from photospots.models import Photospot
from hotels.models import Hotel
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, "friends/home.html")

def search(request):
    kw = request.GET.get("kw", "")  # 검색어
    # tag = Tag.objects.filter(name__icontains=kw)

    # hotel
    hotel_list = Hotel.objects.all()
    if kw:
        hotel_list = hotel_list.filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
            # Q(tags__in=tag) # 태그 검색
        ).distinct()
    hotel_list = sorted(hotel_list, key=lambda a: -a.user_rating)[:4] # 평점순 정렬

    # photospot
    photospot_list = Photospot.objects.all()
    if kw:
        photospot_list = photospot_list.filter(
            Q(place__icontains=kw) # 이름 검색
            # Q(address__icontains=kw) | # 주소 검색
            # Q(tags__in=tag) # 태그 검색
        ).order_by('-like_users').distinct()

    context = {
        'kw': kw,
        'hotel_list': hotel_list,
        'photospot_list': photospot_list,
        }
    return render(request, "main/search.html", context)