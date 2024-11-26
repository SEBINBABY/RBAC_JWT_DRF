from rest_framework import serializers
from .models import Doctor, Prescription, LabReports


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user', 'department']

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = ['prescription', 'date', 'doctor_name']

    def get_doctor_name(self, obj):
        return obj.doctor.user.username if obj.doctor and obj.doctor.user else None

    def to_representation(self, instance):
        # Prefetch the related doctor
        instance = Prescription.objects.select_related('doctor').get(pk=instance.pk)
        return super().to_representation(instance)


class LabReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReports
        fields = ['lab_report', 'date']