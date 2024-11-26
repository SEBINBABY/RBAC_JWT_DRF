from django.urls import path
from .views import (
    register_user, 
    login_user, 
    logout_user, 
    prescription_list, 
    prescription_detail, 
    lab_reports_list, 
    lab_reports_detail
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/register_user/', register_user, name='register-user'),
    path('api/login_user/',login_user, name='login-user'),
    path('api/logout_user/',logout_user, name='logout-user'),
    path('api/prescription_list/',prescription_list, name='prescription-list'),
    path('api/prescription_detail/<int:id>/',prescription_detail, name='prescription-detail'),
    path('api/lab_reports_list/',lab_reports_list, name='lab_reports-list'),
    path('api/lab_reports_detail/<int:id>/',lab_reports_detail, name='lab_reports-detail'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]