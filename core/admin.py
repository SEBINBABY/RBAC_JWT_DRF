from django.contrib import admin
from .models import Doctor, Prescription, LabReports


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']
    list_per_page = 5
    search_fields = ['user']
    
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'date']
    list_per_page = 5
    search_fields = ['prescription']

@admin.register(LabReports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ['lab_report', 'date']
    list_per_page = 5
    search_fields = ['lab_report']
