from decouple import config

print(config('OPENAI_API_KEY'))

list_tables = config('LIST_TABLES').split(',')

for item in list_tables:
    print(item)