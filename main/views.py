from django.shortcuts import render
from hotels.models import Hotel
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def search(request):
    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get("kw", "")  # 검색어
    hotel_list = Hotel.objects.order_by("-rating")
    # tag = Tag.objects.filter(name__icontains=kw)

    if kw:
        hotel_list = hotel_list.filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
            # Q(tags__in=tag) # 태그 검색
        ).distinct()
        hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬

    paginator = Paginator(hotel_list, 9)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {"hotel_list": page_obj, "page": page, "kw": kw}
    return render(request, "main/search.html", context)