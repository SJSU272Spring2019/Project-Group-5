from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','role')
    ordering = ('username',)
    search_fields = ('username',)

admin.site.register(UserProfile, UserProfileAdmin)
