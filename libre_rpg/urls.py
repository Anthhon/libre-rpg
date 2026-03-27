from django.contrib import admin
from django.urls import path
from apps.core import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_render, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('chat/', views.chat_render, name='chat'),

    path('config/', views.configurations_render, name='configurations'),
]
