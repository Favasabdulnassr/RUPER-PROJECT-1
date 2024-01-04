from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
path('signup/', views.signup, name='signup'),
path('otp_verification/', views.otp_verification, name='otp_verification'),
path('login/',views.login, name ='login'),
path('send_otp/', views.send_6_digit_otp_email, name='send_otp'),
path('logout/', views.logout, name='logout'),

]

