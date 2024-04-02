from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class Error404(TemplateView):
    template_name = "errors/error404.html"


class Error301(TemplateView):
    template_name = "errors/error301.html"
