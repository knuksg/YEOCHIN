from django.shortcuts import render
from .models import Hotel
from main.models import Region, DetailRegion
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