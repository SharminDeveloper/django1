from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUserModel
from django import forms 


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields + ("phone_number", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = UserChangeForm.Meta.fields
class ForgotMyPassword(forms.Form):
    username = forms.CharField(max_length=150)