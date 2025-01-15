from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_seller, name='register_seller'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('login/', views.seller_login, name='seller_login'),
    path('about/', views.about, name='about')
    
]
