from django.shortcuts import render
from .models import Hotel
from main.models import Region, DetailRegion
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def index(request):
    hotels = Hotel.objects.order_by('rating')[:4]
    regions = Region.objects.all()
    context = {
        'hotels': hotels,
        'regions': regions,
    }
    return render(request, "hotels/index.html", context)

def search(request):
    regions = Region.objects.all()

    if request.method == 'POST':
        page = request.GET.get("page", "1")  # 페이지
        kw = request.GET.get("kw", "")  # 검색어
        hotel_list = Hotel.objects.all()
        # tag = Tag.objects.filter(name__icontains=kw)

    try:
        post_region = request.POST.get('region')
        region = Region.objects.get(name=post_region)

        if kw:
            hotel_list = hotel_list.filter(
                Q(name__icontains=kw) | # 이름 검색
                Q(address__icontains=kw) # 주소 검색
                # Q(tags__in=tag) # 태그 검색
            ).filter(region=region).distinct()
            # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬
    except:
        if kw:
            hotel_list = hotel_list.filter(
                Q(name__icontains=kw) | # 이름 검색
                Q(address__icontains=kw) # 주소 검색
                # Q(tags__in=tag) # 태그 검색
            ).distinct()
            # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬
    
    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get("kw", "")  # 검색어
    hotel_list = Hotel.objects.all()
    # tag = Tag.objects.filter(name__icontains=kw)

    if kw:
        hotel_list = hotel_list.filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
            # Q(tags__in=tag) # 태그 검색
        ).distinct()
        # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬

    paginator = Paginator(hotel_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'regions': regions,
        "hotel_list": page_obj, 
        "page": page, 
        "kw": kw
        }
    return render(request, "hotels/search.html", context)

def search(request):
    regions = Region.objects.all()

    if request.method == 'POST':
        page = request.GET.get("page", "1")  # 페이지
        kw = request.GET.get("kw", "")  # 검색어
        hotel_list = Hotel.objects.all()
        # tag = Tag.objects.filter(name__icontains=kw)

    try:
        post_region = request.POST.get('region')
        region = Region.objects.get(name=post_region)

        if kw:
            hotel_list = hotel_list.filter(
                Q(name__icontains=kw) | # 이름 검색
                Q(address__icontains=kw) # 주소 검색
                # Q(tags__in=tag) # 태그 검색
            ).filter(region=region).distinct()
            # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬
    except:
        if kw:
            hotel_list = hotel_list.filter(
                Q(name__icontains=kw) | # 이름 검색
                Q(address__icontains=kw) # 주소 검색
                # Q(tags__in=tag) # 태그 검색
            ).distinct()
            # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬
    
    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get("kw", "")  # 검색어
    hotel_list = Hotel.objects.all()
    # tag = Tag.objects.filter(name__icontains=kw)

    if kw:
        hotel_list = hotel_list.filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
            # Q(tags__in=tag) # 태그 검색
        ).distinct()
        # hotel_list = sorted(hotel_list, key=lambda a: -a.rating) # 평점순 정렬

    paginator = Paginator(hotel_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'regions': regions,
        "hotel_list": page_obj, 
        "page": page, 
        "kw": kw
        }
    return render(request, "hotels/search.html", context)


def test(request):
    # 설정한 지역이 있을 때
    post_region = request.GET.get("region", "") # 지역
    if post_region:
        region = Region.objects.get(name=post_region)
    else:
        region = None
    
    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get("kw", "")  # 검색어
    hotel_list = Hotel.objects.all()
    if kw and region:
        hotel_list = hotel_list.filter(region=region).filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
        ).distinct()
    if kw:
        hotel_list = hotel_list.filter(
            Q(name__icontains=kw) | # 이름 검색
            Q(address__icontains=kw) # 주소 검색
        ).distinct()

    paginator = Paginator(hotel_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    region_names = Region.objects.all()
    context = {
        "hotel_list": page_obj, 
        "page": page, 
        "kw": kw,
        "region_names": region_names
        }
    return render(request, "hotels/test.html", context)

def test2(request):
    regions = Region.objects.all()
    if request.method == 'POST':
        post_kw = request.POST.get('kw', '')
        post_region = request.POST.get('region', '')
        post_detail_region = request.POST.get('detail-region', '')
        print(post_kw)
        print(post_region)
        print(post_detail_region)

        if post_kw and post_detail_region:
            detail_region = DetailRegion.objects.get(name=post_detail_region)
            hotels = Hotel.objects.filter(detail_region=detail_region).filter(name__icontains=post_kw)

            context = {
            'hotels': list(hotels.values())[:4],
            }
            return JsonResponse(context)
        elif post_kw and post_region:
            region = Region.objects.get(name=post_region)
            hotels = Hotel.objects.filter(region=region).filter(name__icontains=post_kw)

            context = {
            'hotels': list(hotels.values())[:4],
            }
            return JsonResponse(context)
        elif post_region:
            post_region = request.POST.get('region')
            region = Region.objects.get(name=post_region)

            detail_regions = DetailRegion.objects.filter(region=region)
            hotels = Hotel.objects.filter(region=region)

            context = {
                'detail_region_list': list(detail_regions.values()),
                'hotels': list(hotels.values())[:4],
            }
            return JsonResponse(context)
        elif post_detail_region:
            detail_region = DetailRegion.objects.get(name=post_detail_region)
            hotels = Hotel.objects.filter(detail_region=detail_region)

            context = {
            'hotels': list(hotels.values())[:4],
            }
            return JsonResponse(context)
        elif post_kw:
            hotels = Hotel.objects.filter(name__icontains=post_kw)
            context = {
            'hotels': list(hotels.values())[:4],
            }
            return JsonResponse(context)
            
    context = {
        'regions': regions,
        'hotels': Hotel.objects.all()[:4],
    }
    return render(request, 'hotels/test2.html', context)