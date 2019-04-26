from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_login),
    path('login/', views.my_login),
    path('create_account/', views.create_account),
    path('current_user/', views.get_profile_data),
    path('done/', views.account_confirmed)
]
