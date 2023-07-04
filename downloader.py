import json
import boto3
import base64

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Retrieve the bucket name and image file name from the query parameters
        params = event.get('queryStringParameters', {})
        bucket_name = params.get('bucketname')
        image_file_name = params.get('image')
        
        if not bucket_name or not image_file_name:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid request parameters')
            }
        
        print("Bucket Name:", bucket_name)
        print("Image file name:", image_file_name)
        
        response = s3_client.get_object(Bucket=bucket_name, Key=image_file_name)
        image_file_to_be_downloaded = response['Body'].read()
        
        return {
            'statusCode': 200,
            'body': base64.b64encode(image_file_to_be_downloaded).decode('utf-8'),
            'isBase64Encoded': True
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing required parameter: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

