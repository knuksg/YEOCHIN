from django.shortcuts import render
from .models import Hotel
from main.models import Region, DetailRegion
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def index(request):
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
    return render(request, 'hotels/index.html', context)

def detail(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    context = {
       'hotel': hotel, 
    }
    return render(request, 'hotels/detail.html', context)