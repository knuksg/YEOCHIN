from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path("", views.home, name="home"),
    path("accompany", views.index, name="index"),
    path("accompany2", views.index2, name="index2"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comment/create/", views.comment_create, name="comment_create"),
    path("<int:friend_pk>/<int:comment_pk>/comment/delete/", views.comment_delete, name="comment_delete"),
    path("<int:pk>/like/", views.like, name="like"),
    path("<int:pk>/friend_closed/", views.friend_closed, name="friend_closed"),
    path("index_closed/", views.index_closed, name="index_closed"),
    path("<int:pk>/chat_create/", views.chat_create, name="chat_create"),
    path("<int:pk>/request/", views.request, name="request"),
]
