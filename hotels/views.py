from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, HotelReview, HotelReviewComment
from main.models import Region, DetailRegion
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import HotelReviewForm
from django.contrib.humanize.templatetags.humanize import naturaltime, intcomma
from django.contrib.auth.decorators import login_required

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
            hotels = sorted(hotels, key=lambda x:-x.user_rating)[:4]
            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['pk'] = hotel.pk
                hotel_dict['name'] = hotel.name
                hotel_dict['user_rating'] = hotel.user_rating
                hotel_dict['price'] = intcomma(hotel.price)
                hotel_dict['image'] = hotel.image
                hotels_list.append(hotel_dict)
            context = {
            'hotels': hotels_list,
            }
            return JsonResponse(context)
        elif post_kw and post_region:
            region = Region.objects.get(name=post_region)
            hotels = Hotel.objects.filter(region=region).filter(name__icontains=post_kw)
            hotels = sorted(hotels, key=lambda x:-x.user_rating)[:4]
            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['pk'] = hotel.pk
                hotel_dict['name'] = hotel.name
                hotel_dict['user_rating'] = hotel.user_rating
                hotel_dict['price'] = intcomma(hotel.price)
                hotel_dict['image'] = hotel.image
                hotels_list.append(hotel_dict)
            context = {
            'hotels': hotels_list,
            }
            return JsonResponse(context)
        elif post_region:
            post_region = request.POST.get('region')
            region = Region.objects.get(name=post_region)
            detail_regions = DetailRegion.objects.filter(region=region)
            hotels = Hotel.objects.filter(region=region)
            hotels = sorted(hotels, key=lambda x:-x.user_rating)[:4]
            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['pk'] = hotel.pk
                hotel_dict['name'] = hotel.name
                hotel_dict['user_rating'] = hotel.user_rating
                hotel_dict['price'] = intcomma(hotel.price)
                hotel_dict['image'] = hotel.image
                hotels_list.append(hotel_dict)
            context = {
                'detail_region_list': list(detail_regions.values()),
                'hotels': hotels_list,
            }
            return JsonResponse(context)
        elif post_detail_region:
            detail_region = DetailRegion.objects.get(name=post_detail_region)
            hotels = Hotel.objects.filter(detail_region=detail_region)
            hotels = sorted(hotels, key=lambda x:-x.user_rating)[:4]
            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['pk'] = hotel.pk
                hotel_dict['name'] = hotel.name
                hotel_dict['user_rating'] = hotel.user_rating
                hotel_dict['price'] = intcomma(hotel.price)
                hotel_dict['image'] = hotel.image
                hotels_list.append(hotel_dict)
            context = {
            'hotels': hotels_list,
            }
            return JsonResponse(context)
        elif post_kw:
            hotels = Hotel.objects.filter(name__icontains=post_kw)
            hotels = sorted(hotels, key=lambda x:-x.user_rating)[:4]
            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['pk'] = hotel.pk
                hotel_dict['name'] = hotel.name
                hotel_dict['user_rating'] = hotel.user_rating
                hotel_dict['price'] = intcomma(hotel.price)
                hotel_dict['image'] = hotel.image
                hotels_list.append(hotel_dict)
            context = {
            'hotels': hotels_list,
            }
            return JsonResponse(context)
    context = {
        'regions': regions,
        'hotels': sorted(Hotel.objects.all(), key=lambda x:-x.user_rating)[:4]
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

@login_required
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
    profile_image = review.user.profile.image
    print(profile_image)
    comments = HotelReviewComment.objects.filter(review=review_pk).order_by('created_at')
    context = {
        'hotel': hotel,
        'other_hotels': other_hotels,
        'review': review,
        'comments': comments,
    }
    return render(request, 'hotels/review_detail.html', context)

@login_required
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

@login_required
def review_delete(request, pk, review_pk):
    review = get_object_or_404(HotelReview, pk=review_pk)
    review.delete()
    return redirect('hotels:detail', pk)

def review_like(request, pk, review_pk):
    if request.user.is_authenticated:
        review = HotelReview.objects.get(pk=review_pk)
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
            is_liked = False
        else:
            review.like_users.add(request.user)
            is_liked = True
        data = {
            'is_liked': is_liked,
            'like_count': review.like_users.count(),
        }
    else:
        return redirect('hotels:review_detail', review.pk)
    return JsonResponse(data)

@login_required
def review_comment_create(request, pk, review_pk):
    review = get_object_or_404(HotelReview, pk=review_pk)

    if request.method == 'POST':
        comment = request.POST.get('content', '')
        HotelReviewComment.objects.create(user=request.user, review=review, content=comment)
        comments = HotelReviewComment.objects.filter(review=review_pk).order_by('created_at')
        comment_list = []
        for comment in comments:
            comment_dict = {}
            comment_dict['hotel_pk'] = pk
            comment_dict['review_pk'] = review_pk
            comment_dict['pk'] = comment.id
            comment_dict['user'] = comment.user.username
            comment_dict['user_id'] = comment.user.id
            comment_dict['request_user_id'] = request.user.id
            comment_dict['content'] = comment.content
            comment_dict['created_at'] = naturaltime(comment.created_at)
            comment_dict['updated_at'] = naturaltime(comment.updated_at)
            comment_list.append(comment_dict)
        data = {
            # 'comments': list(comments.values()),
            'comment_list': comment_list,
        }
        return JsonResponse(data)

@login_required
def review_comment_delete(request, pk, review_pk, comment_pk):
    comment = get_object_or_404(HotelReviewComment, pk=comment_pk)
    comment.delete()
    comments = HotelReviewComment.objects.filter(review=review_pk).order_by('created_at')
    comment_list = []
    for comment in comments:
        comment_dict = {}
        comment_dict['hotel_pk'] = pk
        comment_dict['review_pk'] = review_pk
        comment_dict['pk'] = comment.id
        comment_dict['user'] = comment.user.username
        comment_dict['user_id'] = comment.user.id
        comment_dict['request_user_id'] = request.user.id
        comment_dict['content'] = comment.content
        comment_dict['created_at'] = naturaltime(comment.created_at)
        comment_dict['updated_at'] = naturaltime(comment.updated_at)
        comment_list.append(comment_dict)
    data = {
        # 'comments': list(comments.values()),
        'comment_list': comment_list,
    }
    return JsonResponse(data)