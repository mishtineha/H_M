from django.shortcuts import render
from Hospital_app.forms import Signin_doctor,Signin_patient,Login
from django.views.generic.base import View,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django .template import loader
from Hospital_app.models import Doctor,Patient,Appointments,Payment,Hr,Receptionist,Prescription
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from datetime import datetime
from Hospital_project.settings import BASE_DIR
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
                return HttpResponseRedirect('../doctor/')
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
                    p = Patient.objects.filter(user=request.user)
                    d = Doctor.objects.filter(user=request.user)
                    h = Hr.objects.filter(user=request.user)
                    r = Receptionist.objects.filter(user=request.user)
                    if len(p) == 1:
                        return HttpResponseRedirect('../patient/')
                    elif len(d) == 1:
                        return HttpResponseRedirect('../doctor/')
                    elif len(h) == 1:
                        return HttpResponseRedirect('../hr/')
                    elif len(r) == 1:
                        return HttpResponseRedirect('../receptionist/')
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
            try:
                request.user.patient
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")

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
            return HttpResponseRedirect("../home/")

class Patient_appointment(View):
    def get(self,request):
        if request.user.is_active:
            try:
                request.user.patient
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
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
            try:
                request.user.patient
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
            p = Patient.objects.filter(user=request.user)
            pay = Payment.objects.filter(patient = p[0])
            context = {'payment':pay}
            template = loader.get_template('patient_payment.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("LOGIN FIRST")

def Getbill(request,parameter):
    if request.user.is_authenticated:
        count = 0
        try:
            request.user.patient
        except ObjectDoesNotExist:
            count +=1
        try:
            request.user.hr
        except ObjectDoesNotExist:
            count += 1
        if count == 2:
            return HttpResponse("LOGIN FIRST")
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
            is_recep = False
            is_pat = False
            is_hr = False
            p = Patient.objects.filter(user = request.user)
            d = Doctor.objects.filter(user = request.user)
            h = Hr.objects.filter(user = request.user)
            r = Receptionist.objects.filter(user = request.user)
            if len(p) == 1:
                data = p
                is_pat = True
            elif len(d) == 1:
                is_doc = True
                data = d
            elif len(h) == 1:
                data = h
                is_hr = True
            elif len(r) == 1:
                data = r
                is_recep = True
            context = {'data':data[0],'is_doc':is_doc,'is_recep':is_recep,'is_pat':is_pat,'is_hr':is_hr}
            template = loader.get_template('get_profile.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("LOGIN FIRST")

    def post(self,request):
        is_doc = False
        is_recep = False
        is_pat = False
        is_hr = False
        p = Patient.objects.filter(user=request.user)
        d = Doctor.objects.filter(user=request.user)
        h = Hr.objects.filter(user=request.user)
        r = Receptionist.objects.filter(user=request.user)
        if len(p) == 1:
            data = p
            is_pat = True
        elif len(d) == 1:
            is_doc = True
            data = d
        elif len(h) == 1:
            data = h
            is_hr = True
        elif len(r) == 1:
            data = r
            is_recep = True
        data = data[0]
        if is_doc:
            form = Signin_doctor(request.POST)
        else:
            form = Signin_patient(request.POST)
        if form.is_valid:
            data.Name = request.POST['Name']
            data.Email = request.POST['Email']
            data.gender = request.POST['gender3']
            data.phone_no = int(request.POST['phone_no'])
            if is_doc:
                data.Degree = request.POST['degree']
                data.specialization = request.POST['specialization']
            data.save()
        else:
            context = {'data': data, 'is_doc': is_doc,'is_recep':is_recep,'is_pat':is_pat,'is_hr':is_hr}
            template = loader.get_template('get_profile.html')
            return HttpResponse("INVALID DATA " + template.render(context, request))
        return HttpResponseRedirect("../profile/")

class Doctor_view(View):
    def get(self,request):
        if request.user.is_authenticated:
            try:
                request.user.doctor
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
            context = {'nothing':'nothing'}
            template = loader.get_template("doctor_home.html")
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("LOGIN FIRST")

class Hr_view(View):
    def get(self,request):
        if request.user.is_active:
            try:
                request.user.hr
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        context = {'nothing':"nothing"}
        template = loader.get_template("Hr_home.html")
        return HttpResponse(template.render(context,request))

class Recep_view(View):
    def get(self,request):
        if request.user.is_active:
            try:
                request.user.receptionist
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        context = {'nothing': "nothing"}
        template = loader.get_template('recep_home.html')
        return HttpResponse(template.render(context, request))



class Doctor_appointment(View):
    def get(self,request):
        if request.user.is_active:
            try:
                request.user.doctor
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
            d = Doctor.objects.filter(user=request.user)
            appointments = Appointments.objects.filter(doctor=d[0])
            context = {'app':appointments}
            template = loader.get_template('doctor_appointment.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("LOGIN FIRST")

class prescribe(View):
    def get(self,request):
        if request.user.is_active:
            try:
                request.user.doctor
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
            pres = Prescription.objects.filter(Doc = request.user.doctor)
            pat = Patient.objects.all()
            context = {'pres':pres,'pat':pat}
            template = loader.get_template("prescription.html")
            return HttpResponse(template.render(context,request))
    def post(self,request):
        p = Patient.objects.get(user__username = request.POST['username'])
        d = Doctor.objects.get(user = request.user)
        pres = Prescription(patient = p,Doc=d,symptoms = request.POST['symptoms'],
                            medicines = request.POST['medicines'],
                            Dosage = request.POST['dosage'],
                            Duration = request.POST['duration'])
        pres.save()
        return HttpResponseRedirect("../pres/")


class Manage(View):
    def get(self,request,data):
        if request.user.is_active:
            try:
                request.user.receptionist
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        if data == "getall":
            template = loader.get_template("manage_appointment.html")
            pat = Patient.objects.all()
            doc = Doctor.objects.all()
            a = Appointments.objects.all()
            context = {'all_app':a,'pat': pat, 'doc': doc,'is_update':False}
            return HttpResponse(template.render(context, request))
        else:
           try:
               id = int(data)
               all_a = Appointments.objects.all()
               a = Appointments.objects.get(id = id)
               date = str(a.Date_time.date())
               time = a.Date_time.strftime("%H")+":"+a.Date_time.strftime("%M")
               template = loader.get_template("manage_appointment.html")
               pat = Patient.objects.all()
               doc = Doctor.objects.all()
               context = {'all_app': all_a,'app':a,'pat': pat, 'doc': doc, 'is_update': True,'date':date,'time':time,}
               return HttpResponse(template.render(context, request))
           except:
               return HttpResponse("URL DOES NOT Exist")


class Add(View):
    def post(self,request):
        if request.user.is_active:
            try:
                request.user.receptionist
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        id = None
        try:
            id = request.POST["id"]
        except KeyError:
            pass
        date_time = request.POST['date'] + " " + request.POST['time']
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        p = Patient.objects.get(user__username=request.POST['patient_username'])
        d = Doctor.objects.get(user__username=request.POST['doctor_username'])
        status = request.POST['status']

        if id:
            a = Appointments.objects.get(id = id)
            a.patient = p
            a.doctor = d
            a.Date_time = date_time
            a.status = status
            a.save()
            return HttpResponseRedirect("../manage/getall/")
        else:
            a = Appointments(patient = p,doctor = d,Date_time = date_time,status = status)
            a.save()
            return HttpResponseRedirect("../manage/getall/")


class Payment_view(View):
    def get(self, request, data):
        if request.user.is_active:
            try:
                request.user.hr
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        if data == "getall":
            template = loader.get_template("manage_payment.html")
            pat = Patient.objects.all()
            pay = Payment.objects.all()
            context = {'all_pay': pay, 'pat': pat,'is_update': False}
            return HttpResponse(template.render(context, request))
        else:
            try:
                id = int(data)
                all_pay = Payment.objects.all()
                pay = Payment.objects.get(id=id)
                template = loader.get_template("manage_payment.html")
                pat = Patient.objects.all()
                context = {'all_pay': all_pay, 'pay': pay, 'pat': pat,'is_update': True}
                return HttpResponse(template.render(context, request))
            except:
                return HttpResponse("URL DOES NOT Exist")

class Add_payment(View):
    def post(self,request):
        if request.user.is_active:
            try:
                request.user.hr
            except ObjectDoesNotExist:
                return HttpResponse("LOGIN FIRST")
        id = None
        try:
            id = request.POST["id"]
        except KeyError:
            pass
        p = Patient.objects.get(user__username=request.POST['patient_username'])
        f = File(open(BASE_DIR + request.POST["invoice"],"rb"))
        if id:

            a = Payment.objects.get(id = id)
            a.patient = p
            a.amount_paid = request.POST["paid"]
            a.total_amount = request.POST["total"]
            a.invoice = f
            a.save()
            return HttpResponseRedirect("../payment/getall/")

        else:
            a = Payment(patient = p,amount_paid = request.POST["paid"],total_amount = request.POST["total"],invoice = request.FILES)
            a.save()
            return HttpResponseRedirect("../payment/getall/")


