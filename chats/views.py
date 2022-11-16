from django.shortcuts import render
from .models import Room, Message


def index(request):
    return render(request, "chats/index.html")

def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chats/rooms.html', {'rooms': rooms})

def room(request, room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room)[0:25]
    context = {
        "room_name": room_name,
        "room": room,
        "messages": messages,
    }
    return render(request, "chats/room.html", context)