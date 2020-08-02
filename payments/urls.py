from django.urls import path, include
from payments import views

urlpatterns = [
    path('donate/', views.donate_home, name="donate_home"),
    path('config/', views.stripe_config, name="stripe_config"),
    path('create-checkout-session/', views.create_checkout_session, name="checkout_session"),
    path('success/', views.success_view, name="success"),
    path('cancelled/', views.cancelled_view, name="cancelled"),
    path('donate/<dono_id>/', views.donate_main, name="donate main"),
]