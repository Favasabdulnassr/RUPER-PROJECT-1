
from django.urls import path
from.import views

urlpatterns = [ 
    path('myaccount/', views.myaccount, name='myaccount'),
    path('updateaccount/',views.update_account,name='updateaccount'),
    path('changepassword/',views.change_password,name='changepassword'),
    path('editaddress/<str:id>',views.edit_address,name='editaddress'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('deleteaddress/<str:id>',views.delete_address,name='deleteaddress'),

    
]

