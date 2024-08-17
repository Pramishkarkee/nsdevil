from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user import models

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'fullname', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': (
            'fullname',
            'user_type',
        )}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_archived',
                'groups', 'user_permissions',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'fullname',
                'password1',
                'password2',
            ),
        }),
    )
    ordering = ('-date_joined',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_archived', 'groups', 'user_type')
    search_fields = ('username', 'fullname', 'email')


@admin.register(models.PortalUser)
class PortalUserAdmin(UserAdmin):
    list_display = (
        'id',
        'email',
        'is_active',
    )


@admin.register(models.TeacherUser)
class ConsultancyUserAdmin(PortalUserAdmin):
    pass


@admin.register(models.StudentUser)
class InstituteUserAdmin(PortalUserAdmin):
    pass


