from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
path('signup/', views.signup, name='signup'),
path('otp_verification/<str:username>/', views.otp_verification, name='otp_verification'),
path('login/',views.login, name ='login'),
path('logout/', views.logout, name='logout'),

]

