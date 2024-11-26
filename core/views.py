from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from .models import Doctor, Prescription, LabReports
from .serializers import DoctorSerializer, PrescriptionSerializer, LabReportSerializer
from rest_framework import status
from .decorators import allowed_users
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta
from django.utils import timezone


@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        # Ensure all required fields are present
        if not all(key in data for key in ['username', 'password', 'email']):
            return Response({"message": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the username or email already exists
        if User.objects.filter(username=data['username']).exists():
            return Response({"message": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({"message": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
        # Create a new user
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])  # Hash the password
        )
        user.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

@api_view(['POST'])
def login_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        # Set the refresh token in the cookie
        response = Response({
            'access': access_token,
            'message': "Login successful"
        }, status=status.HTTP_200_OK)
        # Set cookie with refresh token, expires in 7 days (you can adjust the expiration time)
        response.set_cookie(
            'refresh_token', refresh_token,
            httponly=True,  # Prevent access to cookie from JS
            secure=True,    # Use secure cookies in production (make sure to use https)
            expires=timezone.now() + timedelta(days=7),  # Expiry time
            samesite='Strict' ) # Prevents the cookie from being sent in cross-site requests
        return response         
    else:
        return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_user(request):
    try:
        # Retrieve the refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')   
        if not refresh_token:
            return Response({"message": "No refresh token found in cookies"}, status=status.HTTP_400_BAD_REQUEST)
        # Blacklist the token
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the token     
        # Remove the refresh token from the cookie
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')  # Remove the cookie
        return response
    except Exception as e:
        return Response({"error": "Invalid token or token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@allowed_users(allowed_roles=['Doctors'])
@authentication_classes([JWTAuthentication]) 
def prescription_list(request):
    if request.method == 'GET':
        prescription = Prescription.objects.all()
        prescription_serializer = PrescriptionSerializer(prescription, many=True)
        return Response({
            "data" : prescription_serializer.data,
            "status": status.HTTP_200_OK
        })
    elif request.method == 'POST':
        try: 
            data = request.data
        except Exception as e:
            print(e)
            return Response({"message": "Data is not found"})
        prescription_serializer = PrescriptionSerializer(data=data)
        if prescription_serializer.is_valid():
            prescription_serializer.save()
            return Response({
                "data": prescription_serializer.data,
                "status": status.HTTP_201_CREATED
            })
        else:
            return Response({
                "Errors": prescription_serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

@api_view(['GET', 'PUT', 'DELETE'])
@allowed_users(allowed_roles=['Doctors'])
@authentication_classes([JWTAuthentication]) 
def prescription_detail(request, id):
        try:
            prescription = Prescription.objects.get(id=id)
        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            prescription_serializer = PrescriptionSerializer(prescription)
            return Response(prescription_serializer.data)
        elif request.method == 'PUT':
            prescription_serializer = PrescriptionSerializer(prescription, data=request.data)
            if prescription_serializer.is_valid():
                prescription_serializer.save()
                return Response(prescription_serializer.data)
            return Response(prescription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            prescription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@allowed_users(allowed_roles=['Doctors','Nurses','Lab Technicians'])
@authentication_classes([JWTAuthentication]) 
def lab_reports_list(request):
    if request.method == 'GET':
        lab_reports = LabReports.objects.all()
        lab_reports_serializer = LabReportSerializer(lab_reports, many=True)
        return Response({
            "data" :  lab_reports_serializer.data,
            "status": status.HTTP_200_OK
        })
    elif request.method == 'POST':
        try: 
            data = request.data
        except Exception as e:
            print(e)
            return Response({"message": "Data is not found"})
        lab_reports_serializer = LabReportSerializer(data=data)
        if lab_reports_serializer.is_valid():
            lab_reports_serializer.save()
            return Response({
                "data": lab_reports_serializer.data,
                "status": status.HTTP_201_CREATED
            })
        else:
            return Response({
                "Errors":lab_reports_serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

@api_view(['GET', 'PUT', 'DELETE'])
@allowed_users(allowed_roles=['Lab Technicians'])
@authentication_classes([JWTAuthentication]) 
def lab_reports_detail(request, id):
        try:
            lab_report = LabReports.objects.get(id=id)
        except LabReports.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            lab_reports_serializer = LabReportSerializer(lab_report)
            return Response(lab_reports_serializer.data)
        elif request.method == 'PUT':
            lab_reports_serializer = LabReportSerializer(lab_report, data=request.data)
            if lab_reports_serializer.is_valid():
                lab_reports_serializer.save()
                return Response(lab_reports_serializer.data)
            return Response(lab_reports_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            lab_report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


