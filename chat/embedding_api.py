import boto3

def get_embedding(text):
    client = boto3.client('comprehend')
    response = client.batch_detect_dominant_language(
        TextList=[text]
    )
    return response['ResultList'][0]['Languages'][0]['LanguageCode']

def embed_rows(rows):
    embeddings = []
    for row in rows:
        concatenated_text = " ".join(str(value) for value in row)
        embedding = get_embedding(concatenated_text)
        embeddings.append(embedding)
    return embeddings
