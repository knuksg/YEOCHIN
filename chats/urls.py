from django.urls import path

from . import views

app_name = "chats"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/rooms/", views.rooms, name="rooms"),
    path("<str:room_name>/", views.room, name="room"),
]