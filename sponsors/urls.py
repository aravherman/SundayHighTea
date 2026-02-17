from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/', views.book_hightea, name='book_hightea'),
]
