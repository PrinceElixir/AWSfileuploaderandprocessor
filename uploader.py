import json
import base64
import boto3
import uuid
import datetime

# Import the necessary libraries for DynamoDB operations
import boto3

client = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    
    # Generate a unique key using a timestamp and UUID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())
    
    # Retrieve the content type of the uploaded file if available, otherwise use a default value
    headers = event.get('headers', {})
    content_type = headers.get('Content-Type', 'application/octet-stream')
    
    # Determine the file extension based on the content type
    file_extension = content_type.split('/')[-1]
    
    key = f"uploads/{timestamp}_{unique_id}.{file_extension}"
    
    # Decode the base64-encoded file data
    ms = base64.b64decode(event['body'])
    
    # Upload the file to S3 with the generated key
    response = client.put_object(
        Body=ms,
        Bucket='me1bucket',
        Key=key
    )
    
    print(response)
    
    # Save file metadata in DynamoDB
    save_metadata_in_dynamodb(key, content_type, timestamp)
    
    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully')
    }

def save_metadata_in_dynamodb(key, content_type, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'myTable'
    table = dynamodb.Table(table_name)
    
    item = {
        'FileKey': key,
        'ContentType': content_type,
        'Timestamp': timestamp
    }
    
    response = table.put_item(Item=item)
    
    print(response)
