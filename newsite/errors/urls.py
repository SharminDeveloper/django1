from django.urls import path
from . import views

urlpatterns = [
    path("404/", views.Error404.as_view(), name="error404"),
    path("301/", views.Error301.as_view(), name="error301"),
]
