from django.urls import path
from . import views

app_name = "hotels"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    # path("<int:pk>/reviews", views.reviews, name="reviews"),
    path("<int:pk>/reviews/create", views.review_create, name="review_create"),
]
