from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, HotelReview
from main.models import Region, DetailRegion
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import HotelReviewForm

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
        'hotels': Hotel.objects.order_by('-rating')[:4],
    }
    return render(request, 'hotels/index.html', context)

def detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    reviews = hotel.hotelreview_set.all()
    context = {
       'hotel': hotel, 
       'reviews': reviews,
    }
    return render(request, 'hotels/detail.html', context)

def review_create(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotels:detail', pk)
    else:
        form = HotelReviewForm()
    context = {
        'hotel': hotel,
        'form': form,
    }
    return render(request, 'hotels/review_create.html', context)

def review_detail(request, pk, review_pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    other_hotels = Hotel.objects.filter(detail_region=hotel.detail_region).exclude(pk=pk)[:5]
    review = get_object_or_404(HotelReview, pk=review_pk)
    context = {
        'hotel': hotel,
        'other_hotels': other_hotels,
        'review': review,
    }
    return render(request, 'hotels/review_detail.html', context)

def review_update(request, pk, review_pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    review = get_object_or_404(HotelReview, pk=review_pk)
    if request.method == 'POST':
        form = HotelReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotels:review_detail', pk, review_pk)
    else:
        form = HotelReviewForm(instance=review)
    context = {
        'hotel': hotel,
        'form': form,
    }
    return render(request, 'hotels/review_create.html', context)

def review_delete(request, pk, review_pk):
    review = get_object_or_404(HotelReview, pk=review_pk)
    review.delete()
    return redirect('hotels:detail', pk)