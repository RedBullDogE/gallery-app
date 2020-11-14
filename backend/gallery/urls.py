from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register),


    path('create/', views.picture_create),  # CREATE
    path('list/', views.picture_list),  # READ | list
    path('list/<int:pk>/', views.picture_details),  # READ | details
    path('update/<int:pk>/', views.picture_change),  # UPDATE
    path('delete/<int:pk>/', views.picture_delete),  # DELETE
]
