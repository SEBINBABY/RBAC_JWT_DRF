# Django Hospital Management System:

A Hospital Management System (HMS) built using Django and Django REST Framework. This system manages Doctor profiles, allowes Role Based Access Control to Doctor's Prescriptions and Lab Reports.

## Table of Contents

* Features

* Technical Requirements

* Installation

* Usage

* API Documentation

## Features

### 1. Authentication and Authorization:

* Implemented an authentication system where users can register, log in, and log out securely using JWTAuthentication.

### 2. Doctor's Prescription Management:

* Create, retrieve, update, and delete prescriptions.
  
* Allowing only Doctors' Role to perform CRUD Operations on Prescriptions.

### 3.  Lab Reports Management:

* Create, retrieve, update, and delete Lab Reports.
  
* Allowing Doctors, Nurses and Lab Technicians Role to Create and retrieve Lab Reports.
  
* Allowing Only Lab Technicians Role to update, and delete Lab Reports.
  

## Technical Requirements

* Django (latest stable version)

* Django REST Framework (latest stable version)

* JWT Authentication

* PEP 8 compliant code

* Comprehensive data validations

* Django ORM for database interactions

## Installation

#### 1.Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate

#### 2. Install dependencies:

pip install Django==5.1.3

pip install -U djangorestframework (Version : 3.15.2 is used here)

pip install djangorestframework-simplejwt (Version : 5.3.1 is used here)                 

#### 3. Run migrations:

python manage.py makemigrations

python manage.py migrate

#### 4. Run:

python manage.py runserver

## API

```bash

http://127.0.0.1:8000/admin/

http://127.0.0.1:8000/api/register_user/

http://127.0.0.1:8000/api/login_user/

http://127.0.0.1:8000/api/logout_user/

http://127.0.0.1:8000/api/prescription_list/

http://127.0.0.1:8000/api/prescription_detail/<int:id>/

http://127.0.0.1:8000/api/lab_reports_list/

http://127.0.0.1:8000/api/lab_reports_detail/<int:id>/

http://127.0.0.1:8000/api/token/refresh/

## API Documentation

Please refer to this documentation for detailed information about each API endpoint, including input parameters, authentication requirements, and response formats.

Sample JSON for registering a user
{
"username" : "Doctor_11",
"password" : "hospital11",
"email" : "doctor11@gmail.com"
}
Sample JSON for login
{
"username" : "Doctor_11",
"password" : "hospital11"
}

## Prescription Endpoints

### 1.Create a prescription(Role Based Access Control given only to Doctor's Role):

URL: POST /api/prescription_list/ Payload Example:

    json

    {
        "prescription": "Take UltraSound for Abdomen"
    }

*Authentication: JWT authentication required.

### 2. List all prescriptions(Role Based Access Control given only to Doctor's Role):

URL: GET /api/prescription_list/

Authentication: JWT authentication required.

Retrieve a specific prescription's details(Role Based Access Control given only to Doctor's Role):

URL: GET /api/prescription_detail/<int:id>/

Authentication: JWT authentication required.

Update a prescription's details(Role Based Access Control given only to Doctor's Role):

URL: PUT /api/prescription_detail/<int:id>/

Payload Example:

json
 
{
"prescription": "Diabetic Tablet"
}

*Authentication: JWT authentication required.

### 3. Delete a prescription(Role Based Access Control given only to Doctor's Role):

URL: DELETE /api/prescription_detail/<int:id>/

Authentication: JWT authentication required.

## Lab Reports Endpoints

### 1. Create a new lab report(Role Based Access Control given to Doctors', Nurses' and Lab Technicians' Role):

URL: POST /api/lab_reports_list/

Payload Example:
json

{
"lab_report": "HypoThyroidism"
}

*Authentication: JWT authentication required.

### 2. List all lab reports(Role Based Access Control given to Doctors', Nurses' and Lab Technicians' Role):

URL: GET /api/lab_reports_list/

Authentication: JWT authentication required.

### 3. Retrieve details of a specific lab report(Role Based Access Control given only to Lab Technicians' Role):

URL: GET /api/lab_reports_detail/<int:id>/

Authentication: JWT authentication required.

Update a lab report(Role Based Access Control given only to Lab Technicians' Role):

URL: PUT /api/lab_reports_detail/<int:id>/

Payload Example:

json

{

"lab_report": "High Cholestrol"

}

*Authentication: JWT authentication required.

### 4. Delete a lab report(Role Based Access Control given only to Lab Technicians' Role:

URL: DELETE /api/lab_reports_detail/<int:id>/

*Authentication: JWT authentication required.

*Authentication: JWT authentication required. Please note that you should replace <int:id> in the URLs with the actual prescription and lab report IDs you want to interact with.

Ensure you have the appropriate authentication token and include it in the Authorisation with Type as Bearer Token and Access Token Value as Token Value for endpoints that require authentication. Also, adjust the payload examples based on the actual structure and requirements of your Django application.

