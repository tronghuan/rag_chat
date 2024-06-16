import requests
from django.http import JsonResponse
import openai
from decouple import config

# Đặt API key của bạn tại đây
openai.api_key = config('OPENAI_API_KEY')


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

def check_milk_name(input_text):
    prompt = f"Is '{input_text}' a brand name of milk? Answer with 'yes' or 'no'."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0
    )

    answer = response.choices[0].text.strip().lower()

    if answer == 'yes':
        return "Bạn muốn mua sữa này size bao nhiêu"
    else:
        return "Nội dung bạn nhập không phải tên của sữa hãy nhập lại."

    # Ví dụ sử dụng
    input_text = "Vinamilk"
    result = check_milk_name(input_text)
    print(result)

    input_text = "Không phải sữa"
    result = check_milk_name(input_text)
    print(result)