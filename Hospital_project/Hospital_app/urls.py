from Hospital_app.views import Signin,Home,Login_view,Patient_home,Logout,Patient_appointment,Patient_invoice,\
    Profile_patient,Doctor_view,Hr_view,Recep_view,Doctor_appointment,prescribe
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'Hospital_app'
urlpatterns =[
    url(r'^$',Signin.as_view(),name='signup'),
    path('home/',Home.as_view(),name = 'Home'),
    path('login/',Login_view.as_view(),name = 'Login'),
    path('patient/',Patient_home.as_view(),name = 'patient_home'),
    path('logout/',Logout.as_view(),name='logout'),
    path('appointment/',Patient_appointment.as_view(),name='patient_appointment'),
    path('invoice/',Patient_invoice.as_view(),name = 'payment'),
    url(r'getbill/(?P<parameter>[0-9]+)/$',views.Getbill,name = 'getbill'),
    url(r'profile/',Profile_patient.as_view(),name = "patient_profile"),
    url(r'doctor/',Doctor_view.as_view(),name = "doctor"),
    url(r'hr/', Hr_view.as_view(), name="hr"),
    url(r'receptionist/', Recep_view.as_view(), name="receptionist"),
    url(r'app_doctor',Doctor_appointment.as_view(),name="app_doctor"),
    url(r'pres/',prescribe.as_view(),name="pres"),


             ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)