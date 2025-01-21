from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_seller, name='register_seller'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('login_and_redirect_to_create_ticket/', views.login_and_redirect_to_create_ticket, name='login_and_redirect_to_create_ticket'),
    path('login_and_redirect_to_my_tickets/', views.login_and_redirect_to_my_tickets, name='login_and_redirect_to_my_tickets'),
    path('about/', views.about, name='about'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='tickets/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='tickets/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tickets/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='tickets/password_reset_complete.html'), name='password_reset_complete'),
]