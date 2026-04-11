from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.core import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_render, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('chat/', views.chat_render, name='chat'),
    path('players/', views.players_list_render, name='players_list'),

    path('config/', views.configurations_render, name='config'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
