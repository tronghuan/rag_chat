from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .call_api import call_api

def index(request):
    data = {
        'key1': 'value1',
        'key2': 'value2'
    }
    return JsonResponse(data, safe=False)

def show(request):
    return call_api()