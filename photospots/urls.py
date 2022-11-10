from django.urls import path
from . import views

app_name = "photospots"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:photospot_pk>/", views.detail, name="detail"),
    path("<int:photospot_pk>/update/", views.update, name="update"),
    path("<int:photospot_pk>/delete/", views.delete, name="delete"),
    path("<int:photospot_pk>/like/", views.like, name="like"),
]
