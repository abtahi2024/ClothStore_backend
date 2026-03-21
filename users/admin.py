from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model=User
    list_display=('email','image_tag','first_name', 'last_name','is_active')
    list_filter=('is_staff','is_active')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

    fieldsets=(
        (None,{'fields':('email','password')}),
        ('Personal Info',{"fields": ("first_name", "last_name",'image','address','phone_number')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

    
admin.site.register(User,CustomUserAdmin)