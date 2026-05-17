from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.core import views
from apps.campaigns.views import campaign_list_render, campaign_creator_render
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_render, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('campaign/list/', campaign_list_render, name='campaign_list'),
    path('campaign/new/', campaign_creator_render, name='campaign_creator'),

    path('campaign/<int:id>/chat/', views.chat_render, name='chat'),
    path('campaign/<int:id>/char_sheet/', views.character_sheet_render, name='char_sheet'),
    path('campaign/<int:id>/players/', views.players_list_render, name='players_list'),

    path('campaign/<int:id>/config/', views.configurations_render, name='config'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
