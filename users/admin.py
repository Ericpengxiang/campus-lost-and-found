from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'created_at']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('phone', 'student_id', 'department', 'user_type', 'avatar', 'bio')}),
    )
