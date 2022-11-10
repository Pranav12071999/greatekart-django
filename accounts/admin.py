from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ['first_name','last_name', 'email', 'username', 'last_login', 'date_joined', 'is_active']
    list_display_links = ['first_name','last_name', 'email'] # This will create links for fields where you can go inside detail information
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['-date_joined']
    # We have created custom user account so for that we need to declare below things.
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account,AccountAdmin)