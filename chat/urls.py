from django.urls import path

from . import views

urlpatterns = [
    path('chat/<room_name>/', views.room, name='room'),
]