from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('test/',views.test, name='test'),
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/answers/create/", views.answers_create, name="answers_create"),
    path("<int:qna_pk>/<int:answer_pk>/answers/update/", views.answers_update, name="answers_update"),    
    path("<int:qna_pk>/<int:answer_pk>/answers/delete/", views.answers_delete, name="answers_delete"),
    path("<int:pk>/like/", views.like, name="like"),

]