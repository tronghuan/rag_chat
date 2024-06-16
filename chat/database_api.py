import psycopg2
from django.conf import settings
import boto3
import json

def fetch_records(table_name):
    connection = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    connection.close()
    return records, columns

def get_embedding(text):
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name='ap-northeast-1',

    )

    body = json.dumps({
        "inputText": text,
    })

    model_id = 'amazon.titan-embed-text-v1'  # look for embeddings in the modelID
    accept = 'application/json'
    content_type = 'application/json'

    # Invoke model
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    # Print response
    response_body = json.loads(response['body'].read())
    return response_body.get('embedding')

def detect_language(text):
    client = boto3.client('comprehend')
    response = client.batch_detect_dominant_language(
        TextList=[text]
    )
    return response['ResultList'][0]['Languages'][0]['LanguageCode']

def embed_rows(rows):
    embeddings = []
    for row in rows:
        concatenated_text = " ".join(
            str(value) for index, value in enumerate(row)
            if index not in [row._meta.get_field('embedding').attname, row._meta.get_field('aws_embedding').attname]
        )
        embedding = get_embedding(concatenated_text)
        embeddings.append(embedding)
    return embeddings

def save_embeddings(table_name, embeddings, rows, columns):
    connection = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    cursor = connection.cursor()
    if 'aws_embedding' not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN aws_embedding TEXT")
    for i, embedding in enumerate(embeddings):
        cursor.execute(
            f"UPDATE {table_name} SET embedding = %s WHERE id = %s",
            (embedding, rows[i][0])
        )
    connection.commit()
    connection.close()

def process_table(table_name):
    rows, columns = fetch_records(table_name)
    embeddings = embed_rows(rows)
    save_embeddings(table_name, embeddings, rows, columns)

# List of tables you want to process
tables_to_process = ['table1', 'table2', 'table3']

for table in tables_to_process:
    process_table(table)
