from django.shortcuts import render, redirect
from .models import Room, Message
from .forms import RoomForm


def index(request):
    return render(request, "chats/index.html")

def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chats/rooms.html', {'rooms': rooms})

def room(request, room_name):
    room = Room.objects.get(name=room_name)
    if room.users.filter(pk=request.user.pk).exists():
        messages = Message.objects.filter(room=room)
        context = {
            "room_name": room_name,
            "room": room,
            "messages": messages,
        }
        return render(request, "chats/room.html", context)
    else:
        return redirect('chats:rooms')

def create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        print('성공')
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect("chats:rooms")
    else:
        form = RoomForm()
    context = {"form": form}
    return render(request, "chats/create.html", context)