from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [path("signup/", views.SignUp.as_view(), name="signup"), 
               path('forgot_my_password/',views.forgot_my_password,name='forgot_my_password') ,
               ]
