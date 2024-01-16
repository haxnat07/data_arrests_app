from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'law_firm', 'preferred_arrest_location', 'city')


admin.site.register(User, UserAdmin)