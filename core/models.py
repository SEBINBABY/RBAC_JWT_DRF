from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.ForeignKey(User, related_name='doctors', on_delete=models.CASCADE)
    department = models.CharField(max_length=20, blank=True, null=True)

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='orders', on_delete=models.CASCADE)
    prescription = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

class LabReports(models.Model):
    lab_report = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    
