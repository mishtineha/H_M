from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=1500)
    Email = models.EmailField()
    gender = models.CharField(max_length=1500)
    phone_no = models.BigIntegerField()

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1500)
    Email = models.EmailField()
    gender = models.CharField(max_length=1500)
    phone_no = models.BigIntegerField()
    Degree = models.CharField(max_length=1500)
    specialization = models.CharField(max_length=1500)

class Hr(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1500)
    Email = models.EmailField()
    gender = models.CharField(max_length=1500)
    phone_no = models.BigIntegerField()

class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1500)
    Email = models.EmailField()
    gender = models.CharField(max_length=1500)
    phone_no = models.BigIntegerField()

class Appointments(models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor',on_delete=models.CASCADE)
    Date_time = models.DateTimeField()
    status = models.CharField(max_length=1500)

class Symptoms(models.Model):
    symptom = models.CharField(max_length=1500)

class Medicines(models.Model):
    med = models.CharField(max_length=1500)
    price = models.IntegerField()

class Prescription(models.Model):
    symptoms = models.ForeignKey('Symptoms',on_delete=models.CASCADE)
    medicines = models.ForeignKey('Medicines',on_delete = models.CASCADE)
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    Doc = models.ForeignKey('Doctor',on_delete=models.CASCADE)
    Dosage = models.CharField(max_length=1500)
    Duration = models.CharField(max_length=1500)

class Payment(models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    total_amount = models.FloatField()
    amount_paid = models.FloatField()
    invoice = models.FileField(upload_to='invoice/', null=True, verbose_name="")


# Create your models here.
