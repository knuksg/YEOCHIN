from django.shortcuts import render, redirect
from .forms import PhotospotForm, CommentForm
from .models import Photospot, Photocomment
from friends.models import Friend
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    photospots = Photospot.objects.order_by("-pk")
    lately_f = Friend.objects.order_by("-pk")[:5]
    context = {
        "photospots": photospots,
        "lately_p": photospots[:5],
        "lately_f": lately_f,
    }
    return render(request, "photospots/index.html", context)


def detail(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    lately_p = Photospot.objects.exclude(pk=photospot_pk).order_by("-pk")[:5]
    lately_f = Friend.objects.order_by("-pk")[:5]
    comment_form = CommentForm()
    context = {
        "photospot": photospot,
        "lately_p": lately_p,
        "lately_f": lately_f,
        "comment_form": comment_form,
        "comments": photospot.photocomment_set.all(),
    }
    return render(request, "photospots/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        photospot_form = PhotospotForm(request.POST, request.FILES)
        if photospot_form.is_valid():
            photospot = photospot_form.save(commit=False)
            photospot.user = request.user
            photospot.save()
            return redirect("photospots:index")
    else:
        photospot_form = PhotospotForm()
    context = {"photospot_form": photospot_form}
    return render(request, "photospots/form.html", context)


@login_required
def update(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    if request.method == "POST":
        photospot_form = PhotospotForm(request.POST, request.FILES, instance=photospot)
        if photospot_form.is_valid():
            photospot_form.save()
            return redirect("photospots:index")
    else:
        photospot_form = PhotospotForm(instance=photospot)
    context = {"photospot_form": photospot_form}
    return render(request, "photospots/form.html", context)


@login_required
def delete(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    photospot.delete()
    return redirect("photospots:index")


@login_required
def like(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    if request.user in photospot.like_users.all():
        photospot.like_users.remove(request.user)
        isLiked = False
    else:
        photospot.like_users.add(request.user)
        isLiked = True
    data = {
        "isLiked": isLiked,
        "likeCount": photospot.like_users.count(),
    }
    return JsonResponse(data)


@login_required
def comment_create(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.photospot = photospot
        comment.user = request.user
        comment.save()
    return redirect("photospots:detail", photospot.pk)


@login_required
def comment_delete(request, comment_pk, photospot_pk):
    comment = Photocomment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("photospots:detail", photospot_pk)
