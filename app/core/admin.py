from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','name']
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_saff', 'is_superuser' )
            }
        ),
        (_('Important dates'), {'fields': ('last login',)})
    )
    
admin.site.register(models.User, UserAdmin)