"""
URL configuration for django_quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from levelup import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('domain/', views.domain, name='domain'),
    path('technology/', views.technology, name='technology'),
    path('add_question/', views.add_question, name='add_question'),
    path('search/', views.search, name='search'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('Thankyou/', views.Thankyou, name='Thankyou'),
    path('Rewards/', views.rewards, name='rewards'),
    path('Feedback/', views.feedback, name='feedback'),
]

