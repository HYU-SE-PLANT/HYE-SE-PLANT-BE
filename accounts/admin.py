from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


# Register your models here.
class UserCheck(UserAdmin):
    list_display = ('account_id', 'user_name', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('account_id', 'user_name')
    ordering = ('-date_joined',)
    
    # admin 페이지에서 사용자 수정할 때 입력폼
    fieldsets = (
        ('user', {'fields': ('password',)}),
        ('Personal Info', {'fields': ('user_name',)}),
    )
    
    # admin 페이지에서 사용자 추가할 때 입력폼
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'user_name', 'password1', 'password2')
        }),
    )
    
admin.site.register(User, UserCheck)