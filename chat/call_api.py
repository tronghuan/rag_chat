import requests
from django.http import JsonResponse

def call_api():
    # URL of the API you want to call
    api_url = 'http://127.0.0.1:8000'

    # Make the GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = {
            'key1': 'value1',
            'key2': 'value2'
        }
        return JsonResponse(data, safe=False)
    else:
        # Handle errors
        return JsonResponse({'error': 'Failed to fetch data from external API'}, status=response.status_code)
