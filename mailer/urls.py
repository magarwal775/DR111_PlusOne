from django.urls import include, path
from mailer import views

urlpatterns = [
    path('', views.index, name="index"),
    path('compose/', views.compose_mail, name="compose_mail"),
    path('send/', views.send_mail, name="send_mail"),
]
