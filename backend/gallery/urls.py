from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.picture_list),
    path('list/<int:pk>/', views.picture),
    path('create/', views.create_picture)
]