from django.shortcuts import render, redirect
from .models import Room, Message
from .forms import RoomForm
from accounts.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "chats/index.html")

@login_required
def rooms(request, pk):
    user = User.objects.get(pk=pk)
    rooms = Room.objects.filter(name__icontains=user.username)
    if rooms:
        room_list = []
        for room in rooms:
            room_dict = {}
            room_dict['url'] = room.name
            room_dict['name'] = room.name.split('rnv')[2]
            room_dict['created_at'] = room.name.split('rnv')[3]
            room_dict['users'] = room.users.all()
            try:
                latest_chat = Message.objects.filter(room=room).order_by('-date_added')[0]
                latest_chat_user = latest_chat.user
                room_dict['latest_chat'] = latest_chat.content
                room_dict['latest_chat_user'] = latest_chat_user.username
                try:
                    room_dict['latest_chat_user_img'] = latest_chat_user.profile.image.url
                except:
                    room_dict['latest_chat_user_img'] = None
                room_dict['latest_chat_time'] = str(latest_chat.date_added)
            except:
                room_dict['latest_chat'] = '아직 아무도 채팅을 시작하지 않았습니다.'
                room_dict['latest_chat_time'] = '채팅을 시작해주세요.'
            room_list.append(room_dict)
        room_list = sorted(room_list, key=lambda x:(x['latest_chat_time'], x['created_at']), reverse=True)
        context = {
            'rooms': rooms,
            'room_list': room_list,
        }
        return render(request, 'chats/rooms.html', context)
    else:
        return redirect('main:index')

@login_required
def room(request, room_name):
    room = Room.objects.get(name=room_name)
    friend_pk = room_name.split('rnv')[1]
    if room.users.filter(pk=request.user.pk).exists():
        messages = Message.objects.filter(room=room)
        context = {
            "room_name": room_name,
            "room": room,
            "messages": messages,
            "friend_pk": friend_pk,
            "room_real_name": room_name.split('rnv')[2],
            "room_real_time": room_name.split('rnv')[3],
        }
        return render(request, "chats/room.html", context)
    else:
        return redirect('chats:rooms', request.user.pk)

@login_required
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