from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .call_api import check_milk_name
import json
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def check(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        body = json.loads(request.body)
        user_message = body.get('user_message', 'default_value')
        ai_response = check_milk_name(user_message)
        return JsonResponse({'ai_response': f'{ai_response}'})