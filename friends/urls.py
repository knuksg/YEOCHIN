from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comment/create/", views.comment_create, name="comment_create"),
    path("<int:friend_pk>/<int:comment_pk>/comment/delete/", views.comment_delete, name="comment_delete"),
    path("<int:pk>/like/", views.like, name="like"),



]
