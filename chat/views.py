from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .call_api import call_api

def index(request):
    data = {
        'key1': 'value1',
        'key2': 'value2'
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def show(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())