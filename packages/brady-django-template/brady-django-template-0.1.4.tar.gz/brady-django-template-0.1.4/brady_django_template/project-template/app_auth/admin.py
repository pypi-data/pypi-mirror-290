from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib import auth

admin.site.unregister(auth.models.Group)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['user_id', 'email', 'username', 'last_login_ip'] 

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (
            ('Additional Information', {'fields': ('last_login_ip',)}),
        )
        return fieldsets

admin.site.register(User, CustomUserAdmin)
