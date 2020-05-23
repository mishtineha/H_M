from Hospital_app.views import Signin
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
app_name = 'Hospital_app'
urlpatterns =[
    url(r'^$',Signin.as_view(),name='signup'),
    ]