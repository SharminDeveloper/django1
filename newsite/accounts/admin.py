from django.contrib import admin
from .models import CustomUserModel
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('id',)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age", "phone_number")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age", "phone_number", "email")}),)


admin.site.register(CustomUserModel, CustomUserAdmin)
