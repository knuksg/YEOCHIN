from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/answer/create/", views.answer_create, name="answer_create"),
    path("<int:qna_pk>/<int:answer_pk>/answer/delete/", views.answer_delete, name="answer_delete"),
]