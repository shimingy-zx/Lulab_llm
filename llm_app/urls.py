from django.urls import path
from . import views

urlpatterns = [
    path('', views.QueryChat.as_view()),
    path('file', views.QueryFile.as_view()),
]

