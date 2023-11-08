from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from rest_framework.permissions import IsAuthenticated

urlpatterns = [
    path('', views.index),
    path('forlogin', views.login_view ),
    path('login/', views.TokenObtainPairView.as_view()),    
    path('secret', views.getNotes),
    path('register', views.register),
    path('categories', views.myCategories),
    path('product', views.product_list),
    path('Porder', views.create_order),
    path('user_info/', views.user_info, name='user_info'),  
    path('create_order/', views.CreateOrderView.as_view(), name='create-order')
]
