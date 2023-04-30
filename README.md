
# Blog Application

Blog Application using Django Rest framework


## Features

- User Registration and Login
- Using JWT authentication
- Only Logged User can create, Update and Delete blogs
- Every User can view all the blogs and also search the particular blogs 


## Installation

Create a virtual environment to install dependencies in and activate it

```
  pip install virtualenv

  virtualenv env

  env\scripts\activate
```
Install Django into the virtualenv
```
  pip install django

  pip install djangorestframework
```
Simple JWT can be installed with pip

```
pip install djangorestframework-simplejwt
```
Start the Django server:
```
python manage.py runserver
```
drf-yasg -  Swagger generator
```
pip install -U drf-yasg
```
## Documentation

[Documentation](http://localhost:8000/swagger/)

