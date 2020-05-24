from django.shortcuts import render
from Hospital_app.forms import Signin_doctor,Signin_patient,Login
from django.views.generic.base import View,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django .template import loader
from Hospital_app.models import Doctor,Patient,Appointments,Payment,Hr,Receptionist
from django.contrib.auth.models import User

class Signin(View):
    def get(self,request):
        option = request.GET['q']
        doc = Signin_doctor()
        patient = Signin_patient()
        form = patient
        if option == "1":
            form = doc
        context = {'form':form,'is_alert':False}
        template = loader.get_template('signup.html')
        return HttpResponse(template.render(context,request))

    def post(self,request):
        is_doc = False
        try:
            x = request.POST['Degree']
            form = Signin_doctor(request.POST)
            is_doc = True
        except KeyError:
            form = Signin_patient(request.POST)
            pass

        if request.POST['confirm_password'] !=request.POST['password']:
            context = {'form': form, 'is_alert': True}
            template = loader.get_template('signup.html')
            return HttpResponse("PASSWORD DOES NOT MATCH!<br><br>" + template.render(context, request))
        if form.is_valid():
            user = User(username = request.POST['username'],password = request.POST['password'])
            try:
                user.save()
            except:
                context = {'form': form, 'is_alert': True}
                template = loader.get_template('signup.html')
                return HttpResponse("USERNAME ALREADY EXIST!!!!!!<br><br>" + template.render(context, request))
            user = User.objects.get(username = request.POST['username'])
            login(request,user)
            if is_doc:
                doc = Doctor(user = user,Name = request.POST['Name'],Email = request.POST['Email'],
                             gender= request.POST['gender'],phone_no = request.POST['phone_no'],
                             Degree=request.POST['Degree'],specialization=request.POST['specialization'])
                doc.save()
            else:
                pat = Patient(user = user,Name = request.POST['Name'],Email = request.POST['Email'],
                             gender= request.POST['gender'],phone_no = request.POST['phone_no'])
                pat.save()

            return HttpResponseRedirect('../patient/')
        else:
            context = {'form': form, 'is_alert': True}
            template = loader.get_template('signup.html')
            return HttpResponse(template.render(context, request))

class Home(View):
    def get(self,request):
        context = {'nothing':'nothing'}
        template = loader.get_template('Home.html')
        return HttpResponse(template.render(context, request))

class Login_view(View):
    def get(self,request):
        form = Login
        context = {'form':form,'is_alert':False}
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))
    def post(self,request):
        form = Login(request.POST)
        if form.is_valid:
                user = User.objects.filter(username=str(request.POST['username']),password=str(request.POST['password']))
                if len(user) == 1:
                    login(request,user[0])
                    return HttpResponseRedirect('../patient/')
                else:
                    context = {'form': form,'is_alert':True}
                    template = loader.get_template('login.html')
                    return HttpResponse("<b>username or password does not matcj</b><br>" + template.render(context, request))
        else:
            context = {'form': form,'is_alert':True}
            template = loader.get_template('login.html')
            return HttpResponse("<b>username or password does not match in else</b>" + template.render(context, request))



class Patient_home(View):
    def get(self,request):
        if request.user.is_authenticated:

            context = {"nothing":"nothing"}
            template = loader.get_template('patient_home.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("LOGIN FIRST")

class Logout(View):
    def get(self,request):
        if request.user.is_active:
            logout(request)
            return HttpResponseRedirect("../home/")
        else:
            return HttpResponse("LOGIN FIRST")

class Patient_appointment(View):
    def get(self,request):
        if request.user.is_active:
            p = Patient.objects.filter(user=request.user)
            appointments = Appointments.objects.filter(patient=p[0])
            context = {'app':appointments}
            template = loader.get_template('patient_appointment.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("LOGIN FIRST")

class Patient_invoice(View):
    def get(self,request):
        if request.user.is_active:
            p = Patient.objects.filter(user=request.user)
            pay = Payment.objects.filter(patient = p[0])
            context = {'payment':pay}
            template = loader.get_template('patient_payment.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("LOGIN FIRST")

def Getbill(request,parameter):
    if request.user.is_authenticated:
        pay = Payment.objects.get(id = parameter)
        context = {"url":pay.invoice}
        template = loader.get_template("display_bill.html")
        return HttpResponse(template.render(context,request))
    else:
        return HttpResponse("LOGIN FIRST")

class Profile_patient(View):
    def get(self,request):
        if request.user.is_authenticated:
            is_doc=False
            p = Patient.objects.filter(user = request.user)
            d = Doctor.objects.filter(user = request.user)
            h = Hr.objects.filter(user = request.user)
            r = Receptionist.objects.filter(user = request.user)
            if len(p) == 1:
                data = p
            elif len(d) == 1:
                is_doc = True
                data = d
            elif len(h) == 1:
                data = h
            elif len(r) == 1:
                data = r
            context = {'data':data[0],'is_doc':is_doc}
            template = loader.get_template('get_profile.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("LOGIN FIRST")

    def post(self,request):
        is_doc = False
        p = Patient.objects.filter(user=request.user)
        d = Doctor.objects.filter(user=request.user)
        h = Hr.objects.filter(user=request.user)
        r = Receptionist.objects.filter(user=request.user)
        if len(p) == 1:
            data = p
        elif len(d) == 1:
            is_doc = True
            data = d
        elif len(h) == 1:
            data = h
        elif len(r) == 1:
            data = r
        data = data[0]
        data.Name = request.POST['Name']
        data.Email = request.POST['Email']
        data.gender = request.POST['gender']
        data.phone_no = request.POST['phone_no']
        if is_doc:
            data.Degree = request.POST['degree']
            data.specialization = request.POST['specialization']
        data.save()
        return HttpResponseRedirect("../profile/")








