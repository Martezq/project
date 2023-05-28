from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'email_verified', 'is_active', 'is_staff', 'is_superuser',)
    fieldsets = UserAdmin.fieldsets + (
        ('Email Verification', {'fields': ('email_verified',)}),
    )

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)