from django.urls import path
from . import views

app_name = "hotels"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    # path("<int:pk>/reviews/", views.reviews, name="reviews"),
    path("<int:pk>/reviews/create/", views.review_create, name="review_create"),
    path("<int:pk>/reviews/<int:review_pk>/", views.review_detail, name="review_detail"),
    path("<int:pk>/reviews/<int:review_pk>/like/", views.review_like, name="review_like"),
    path("<int:pk>/reviews/<int:review_pk>/update/", views.review_update, name="review_update"),
    path("<int:pk>/reviews/<int:review_pk>/delete/", views.review_delete, name="review_delete"),
    path("<int:pk>/reviews/<int:review_pk>/comments/create/", views.review_comment_create, name="review_comment_create"),
    path("<int:pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/delete/", views.review_comment_delete, name="review_comment_delete"),
]


