from django.shortcuts import render, redirect
from . models import Friend, Friend_Comment
from . forms import FriendForm,Friend_CommentForm
from django.http import HttpResponseForbidden

# Create your views here.
def index(request):
    friends = Friend.objects.all()
    context = {
        'friends':friends
    }
    return render(request, "friends/index.html",context)

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
        context = {
            "friend_form": friend_form
            }
        return render(request, "friends/create.html", context)
    else:
        return HttpResponseForbidden()

def detail(request, pk):
    friend = Friend.objects.get(pk=pk)
    comments = friend.friend_comment_set.all()
    comment_form = Friend_CommentForm()

    context = {
        "friend":friend,
        "comments":comments,
        "comment_form":comment_form,
    }
    return render(request,"friends/detail.html", context)

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
        context = {
            "friend_form":friend_form
        }
        return render(request, "friends/create.html", context)
    else:
        return HttpResponseForbidden()


def delete(request, pk):
    friend = Friend.objects.get(pk=pk)
    if request.user == friend.user:
        friend.delete()
        return redirect("friends:index")
    else:
        return HttpResponseForbidden()

def comment_create(request, pk):
    friend = Friend.objects.get(pk=pk)
    comment_form = Friend_CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.friend = friend
        comment.user = request.user
        comment.save()

        return redirect("friends:detail", pk)

def comment_delete(request, friend_pk, comment_pk):
    friend = Friend.objects.get(pk=friend_pk)
    comment = Friend_Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return redirect("friends:detail", friend.pk)
    else:
        return HttpResponseForbidden()

def like(request, pk):
    friend = Friend.objects.get(pk=pk)
    if request.user in friend.like_user.all():
        friend.like_user.remove(request.user)
    else:
        friend.like_user.add(request.user)
    return redirect("friends:detail", pk)