from django.shortcuts import render, redirect
from .models import Friend, Friend_Comment, FriendRequest
from .forms import FriendForm, Friend_CommentForm, FriendRoomForm
from chats.forms import RoomForm
from django.http import HttpResponseForbidden
from datetime import date, datetime, timedelta, timezone
from qna.models import Qna
from photospots.models import Photospot
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    friends = Friend.objects.all()
    lately_f = Friend.objects.order_by("-pk")[:4]
    lately_q = Qna.objects.order_by("-pk")[:4]
    best_p = Photospot.objects.all()
    best_p = sorted(best_p, key=lambda a: -a.like_users.count())[:4]
    context = {
        "friends": friends,
        "lately_f": lately_f,
        "lately_q": lately_q,
        "best_p": best_p,
    }
    return render(request, "friends/home.html", context)


def index(request):
    friends = Friend.objects.order_by("-pk")
    sort = request.GET.get("sort", "")
    sort = request.GET.get("test", "All")
    if sort == "Ongoing":
        friends = friends.filter(closed=False)
    elif sort == "End":
        friends = friends.filter(closed=True)
    else:
        friends = Friend.objects.order_by("-pk")
    context = {
        "friends": friends,
    }
    return render(request, "friends/index.html", context)


def index2(request):
    friends = Friend.objects.order_by("-pk")
    sort = request.GET.get("sort", "")
    sort = request.GET.get("test", "All")
    if sort == "Ongoing":
        friends = friends.filter(closed=False)
    elif sort == "End":
        friends = friends.filter(closed=True)
    else:
        friends = Friend.objects.filter(closed=False)
    context = {
        "friends": friends,
    }
    return render(request, "friends/index2.html", context)


def index_closed(request):
    friends = Friend.objects.order_by("-pk")
    status = False
    if request.method == "POST":
        if status == False:
            print(status)
            friends = Friend.objects.order_by("-pk")
            status != status
        else:
            print(status)
            friends = friends.filter(closed=False)
            status != status
    return redirect("friends:index")


def friend_closed(request, pk):
    friend = Friend.objects.get(pk=pk)
    if friend.closed == False:
        friend.closed = True
        friend.save()
    else:
        friend.closed = False
        friend.save()
    return redirect("friends:detail", pk)


@login_required
def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            friend_form = FriendForm(request.POST, request.FILES)
            if friend_form.is_valid():
                friend = friend_form.save(commit=False)
                friend.user = request.user
                friend.save()
                return redirect("friends:index")
        else:
            friend_form = FriendForm()
        context = {"friend_form": friend_form}
        return render(request, "friends/create.html", context)
    else:
        return HttpResponseForbidden()


def detail(request, pk):
    friend = Friend.objects.get(pk=pk)
    comments = friend.friend_comment_set.all()
    comment_form = Friend_CommentForm()
    Dday = (friend.end_at - friend.start_at).days + 1

    context = {
        "friend": friend,
        "comments": comments,
        "comment_form": comment_form,
        "Dday": Dday,
    }
    response = render(request, "friends/detail.html", context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get("hitboard", "_")
    if f"_{pk}_" not in cookie_value:
        cookie_value += f"_{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        friend.hits += 1
        friend.save()

    return response


@login_required
def update(request, pk):
    friend = Friend.objects.get(pk=pk)
    if request.user == friend.user:
        if request.method == "POST":
            friend_from = FriendForm(request.POST, request.FILES, instance=friend)
            if friend_from.is_valid():
                friend_from.save()
                return redirect("friends:detail", pk)
        else:
            friend_form = FriendForm(instance=friend)
        context = {"friend_form": friend_form}
        return render(request, "friends/create.html", context)
    else:
        return HttpResponseForbidden()


@login_required
def delete(request, pk):
    friend = Friend.objects.get(pk=pk)
    if request.user == friend.user:
        friend.delete()
        return redirect("friends:index")
    else:
        return HttpResponseForbidden()


@login_required
def comment_create(request, pk):
    friend = Friend.objects.get(pk=pk)
    comment_form = Friend_CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.friend = friend
        comment.user = request.user
        comment.save()

        return redirect("friends:detail", pk)


@login_required
def comment_delete(request, friend_pk, comment_pk):
    friend = Friend.objects.get(pk=friend_pk)
    comment = Friend_Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return redirect("friends:detail", friend.pk)
    else:
        return HttpResponseForbidden()


@login_required
def like(request, pk):
    friend = Friend.objects.get(pk=pk)
    if request.user in friend.like_user.all():
        friend.like_user.remove(request.user)
    else:
        friend.like_user.add(request.user)
    return redirect("friends:detail", pk)


import lorem
from accounts.models import User
from chats.models import Room

@login_required
def chat_create(request, pk):
    friend = Friend.objects.get(pk=pk)
    friendrequest = FriendRequest.objects.get(friend=friend)
    request_users = friendrequest.users.all()
    if request.method == "POST":
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        room_name_variable = "rnv"
        room_name = (
            request.user.username
            + room_name_variable
            + str(friend.pk)
            + room_name_variable
            + friend.title
            + room_name_variable
            + time
        )
        room = Room(name=room_name)
        room.save()
        selects = request.POST.getlist("member-select")
        for select in selects:
            user = User.objects.get(username=select)
            room.users.add(user)
        return redirect("chats:rooms", request.user.pk)
    context = {"request_users": request_users}
    return render(request, "friends/chat_create.html", context)

@login_required
def request(request, pk):
    friend = Friend.objects.get(pk=pk)
    friendrequest = FriendRequest.objects.get_or_create(friend=friend)
    friendrequest = friendrequest[0]
    friendrequest.users.add(request.user)
    return redirect("friends:detail", pk)
