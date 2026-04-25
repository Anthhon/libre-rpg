from django.contrib import admin
from .models import Profile

# Change main admin site headers
admin.site.site_header = "Libre RPG Admin Page"
admin.site.site_title = "Libre RPG"
admin.site.index_title = "Welcome to the admin page"

admin.site.register(Profile)
