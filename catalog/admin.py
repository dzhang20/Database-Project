from django.contrib import admin

# Register your models here.
from catalog.models import UserProfile

admin.site.register(UserProfile)
