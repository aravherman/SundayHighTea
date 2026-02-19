from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.create_order, name='create_order'),
    path('verify/', views.verify_payment, name='verify_payment'),
]
