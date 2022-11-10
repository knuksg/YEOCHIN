from django.shortcuts import render, redirect
from .forms import PhotospotForm
from .models import Photospot
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    photospots = Photospot.objects.order_by("-pk")
    context = {
        "photospots": photospots,
    }
    return render(request, "photospots/index.html", context)


# @login_required
def create(request):
    if request.method == "POST":
        photospot_form = PhotospotForm(request.POST, request.FILES)
        if photospot_form.is_valid():
            photospot = photospot_form.save(commit=False)
            # photospot.user = request.user
            photospot.save()
            return redirect("photospots:detail", photospot.pk)
    else:
        photospot_form = PhotospotForm()
    context = {"photospot_form": photospot_form}
    return render(request, "photospots/form.html", context)


def detail(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    context = {
        "photospot": photospot,
    }
    return render(request, "photospots/detail.html", context)


# @login_required
def update(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    if request.method == "POST":
        photospot_form = PhotospotForm(request.POST, request.FILES, instance=photospot)
        if photospot_form.is_valid():
            photospot_form.save()
            return redirect("photospots:detail", photospot.pk)
    else:
        photospot_form = PhotospotForm(instance=photospot)
    context = {"photospot_form": photospot_form}
    return render(request, "photospots/form.html", context)


# @login_required
def delete(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    photospot.delete()
    return redirect("photospots:index")


# @login_required
def like(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    if request.user in photospot.like_users.all():
        photospot.like_users.remove(request.user)
    else:
        photospot.like_users.add(request.user)
        isLiked = True
    data = {
        "isLiked": isLiked,
        "likeCount": photospot.like_users.count(),
    }
    return JsonResponse(data)
