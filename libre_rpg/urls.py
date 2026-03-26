"""
URL configuration for libre_rpg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import render


def configurations_render(request):
    return render(request, "configurations.html")


def chat_render(request):
    return render(request, "chat.html")


def dashboard_render(request):
    return render(request, "dashboard.html")


def login_render(request):
    return render(request, "welcome.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_render, name='login'),
    path('chat/', chat_render, name='chat'),
    path('config/', configurations_render, name='configurations'),
]
