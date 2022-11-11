from django.shortcuts import render
from .models import Hotel
from main.models import Region, DetailRegion
from django.http import JsonResponse

# Create your views here.
def index(request):
    hotels = Hotel.objects.order_by('rating')[:4]
    if request.method == 'POST':
        post_region = request.GET.get('region') or '서울'
        region = Region.objects.get(name=post_region)
        detail_regions = DetailRegion.objects.filter(region=region)[0]
        return JsonResponse({
            'detail_regions': detail_regions
        })
    context = {
        'hotels': hotels,
    }
    return render(request, "hotels/index.html", context)