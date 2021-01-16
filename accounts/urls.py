from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('userpage/',userPage,name='user-page'),
    path('settings/',settings,name='settings'),

    #Login register
    path('register/',registerPage,name='register'),
    path('login/',loginPage,name='login'),
    path('logout/',Logoutuser,name='logout'),


    path('',Home,name='home'),
    path('products/',Products,name='products'),
    path('customers/<str:pk_test>/',Clientes,name='customers'),

    #Create

    path('create_order/<str:pk>',CreateOrder,name='create_order'),
    path('create_customer/',CreateCustomer,name='create_customer'),
    


    #Update

    path('update_order/<str:pk>',UpdateOrder,name='update_order'),
    path('update_customer/<str:pk>',UpdateCustomer,name='update_customer'),
    


    #Delete

    path('delete_order/<str:pk>',DeleteOrder,name='delete_order'),
    path('delete_customer/<str:pk>',DeleteCustomer,name='delete_customer'),

    #Reset and Auth

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_complete'),
    
    
]
