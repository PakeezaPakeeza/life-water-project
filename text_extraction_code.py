import os
import json
import logging
import boto3
from urllib.parse import unquote_plus

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    
    # Initialize S3 and Textract clients
    s3 = boto3.client('s3')
    textract = boto3.client('textract')
    
    for record in event.get('Records', []):
        try:
            # Get the bucket and file details
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])
            logger.info(f"Processing file {object_key} from bucket {bucket_name}")
            
            # Call Textract to detect document text
            response = textract.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': object_key
                    }
                }
            )
            
            # Extract all lines of text
            extracted_lines = [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']
            logger.info(f"Extracted lines: {extracted_lines}")
            
            # Save extracted lines to S3
            output_data = {"ExtractedText": extracted_lines}
            output_key = f"output/{os.path.basename(object_key)}.json"
            s3.put_object(
                Bucket=bucket_name,
                Key=output_key,
                Body=json.dumps(output_data, indent=4),
                ContentType="application/json"
            )
            logger.info(f"Saved extracted text to {output_key}")
        
        except Exception as e:
            logger.error(f"Error processing file {object_key} from bucket {bucket_name}: {str(e)}", exc_info=True)
            return {
                "statusCode": 500,
                "body": f"Error: {str(e)}"
            }
    
    return {
        "statusCode": 200,
        "body": "Processing completed successfully"
    }
