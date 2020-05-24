from Hospital_app.views import Signin,Home,Login_view
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
app_name = 'Hospital_app'
urlpatterns =[
    url(r'^$',Signin.as_view(),name='signup'),
    url('home/',Home.as_view(),name = 'Home'),
    url('login/',Login_view.as_view(),name = 'Login')
    ]