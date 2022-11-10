from django.urls import path
from . import views

app_name = "photospots"

urlpatterns = [
    path("", views.index, name="index"),
]
