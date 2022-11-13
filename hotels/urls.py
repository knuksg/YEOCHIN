from django.urls import path
from . import views

app_name = "hotels"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/detail/", views.detail, name="detail"),
]
