# 📦 Store Management (Cloth Store API)

**🛍️ Project Overview**

This is a Django REST based E-commerce backend project.

` It includes: `
- Custom User Authentication (Email)
- JWT Authentication
- Google OAuth Login
- Email Activation System
- Product Management
- Order Management
- SSLCommerz Payment Integration (Sandbox)
- Cloudinary Image Storage
- Swagger API Documentation
- Django Admin Panel
- Debug Toolbar

---
**⚙️ Tech Stack**
- Django 6
- Django REST  Framework
- Djoser
- Simple JWT
Social Auth (Google OAuth2)
- Cloudinary
- drf-yasg (Swagger)
- SQLite Database
- WhiteNoise
---
**📂 Installed Apps**
```
# bash
api
users
product
order
payments
```
***
**Framework & Tools:**
```
- rest_framework
- djoser
- social_django
- drf_yasg
- django_filters
- debug_toolbar
- whitenoise 
```

**🔐 Authentication System**
- Custom User Model (AUTH_USER_MODEL = users.User)
- Email & Password Login
- JWT Token Authentication
- Google OAuth2 Login
- Email Activation Required

## 📘 API Documentation
**Swagger UI:**
http://127.0.0.1:8000/swagger/

## 🗂️ Project Structure
````css
storemanagemant/
│
├── api/
├── users/
├── product/
├── order/
├── payments/
│
├── storemanagemant/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py
````

## ▶️ Run Project

```diff
+ python manage.py makemigrations
- python manage.py migrate
! python manage.py runserver 
```