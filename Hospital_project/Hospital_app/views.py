from django.shortcuts import render
from Hospital_app.forms import Signin_doctor,Signin_patient
from django.views.generic.base import View,HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django .template import loader
from Hospital_app.models import Doctor,Patient
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
                return HttpResponse("username ALREADY EXIST!!!!!!<br><br>" + template.render(context, request))
            user = User.objects.get(username = request.POST['Email'])
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

            return HttpResponse("login succesfully")
        else:
            context = {'form': form, 'is_alert': True}
            template = loader.get_template('signup.html')
            return HttpResponse(template.render(context, request))





