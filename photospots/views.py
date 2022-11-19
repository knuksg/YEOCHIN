from datetime import date, datetime, timedelta, timezone

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from friends.models import Friend

from .forms import CommentForm, PhotospotForm
from .models import Photocomment, Photospot


# Create your views here.
def index(request):
    photospots = Photospot.objects.order_by("-pk")
    best_p = Photospot.objects.all()
    best_p = sorted(best_p, key=lambda a: -a.like_users.count())[:5]
    lately_f = Friend.objects.order_by("-pk")[:5]
    context = {
        "photospots": photospots,
        "best_p": best_p,
        "lately_f": lately_f,
    }
    return render(request, "photospots/index.html", context)


def detail(request, photospot_pk):
    photospot = Photospot.objects.get(pk=photospot_pk)
    best_p = Photospot.objects.exclude(pk=photospot_pk)[:5]
    best_p = sorted(best_p, key=lambda a: -a.like_users.count())
    lately_f = Friend.objects.order_by("-pk")[:5]
    comment_form = CommentForm()

    photospot.hits += 1
    photospot.save()

    context = {
        "photospot": photospot,
        "best_p": best_p,
        "lately_f": lately_f,
        "comment_form": comment_form,
        "comments": photospot.photocomment_set.all(),
    }
    response = render(request, "photospots/detail.html", context)

    return response


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
            photospot.is_updated = True
            photospot = photospot_form.save(commit=False)
            photospot.save()
            return redirect("photospots:index")
    else:
        photospot_form = PhotospotForm(instance=photospot)
    context = {"photospot_form": photospot_form, "photospot": photospot}
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


def best(request):
    best_p = Photospot.objects.all()[:20]
    best_p = sorted(best_p, key=lambda a: -a.like_users.count())
    best_p5 = Photospot.objects.all()[:5]
    best_p5 = sorted(best_p5, key=lambda a: -a.like_users.count())
    lately_f = Friend.objects.order_by("-pk")[:5]
    context = {
        "best_p": best_p,
        "best_p5": best_p5,
        "lately_f": lately_f,
    }
    return render(request, "photospots/best.html", context)
