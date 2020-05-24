from Hospital_app.views import Signin,Home,Login_view,Patient_home,Logout,Patient_appointment
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
app_name = 'Hospital_app'
urlpatterns =[
    url(r'^$',Signin.as_view(),name='signup'),
    path('home/',Home.as_view(),name = 'Home'),
    path('login/',Login_view.as_view(),name = 'Login'),
    path('patient/',Patient_home.as_view(),name = 'patient_home'),
    path('logout/',Logout.as_view(),name='logout'),
    path('appointment/',Patient_appointment.as_view(),name='patient_appointment')
    path('invoice/',)

    ]