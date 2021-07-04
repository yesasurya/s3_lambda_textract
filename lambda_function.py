import csv
import json
import boto3
import base64

from models.block_factory import BlockFactory
from models.csv_builder import CsvBuilder
from models.textract import Textract
from sample_api_response import SAMPLE_API_RESPONSE
from config import DEFAULT_REGION, S3_BUCKET_FOR_CSV


def process_api_response(response):
    block_factory = BlockFactory(response)
    csv_builder = CsvBuilder(block_factory.page_block, block_factory.key_blocks)
    return csv_builder.csv_content


def lambda_handler(event, context):
    try:
        s3_record = event["Records"][0]["s3"]
        s3_bucket_name = s3_record["bucket"]["name"]
        s3_object_name = s3_record["object"]["key"]
    except Exception as e:
        s3_bucket_name, s3_object_name = None, None
    
    if s3_bucket_name is None or s3_object_name is None:
        message = '[ERROR] Failed to get the information about S3 object.'
    else:
        s3_object = {
            'Bucket': s3_bucket_name,
            'Name': s3_object_name
        }

        textract_client = boto3.client('textract', region_name=DEFAULT_REGION)
        textract = Textract(textract_client)
        textract_response = textract.analyze_document(s3_object)
        csv_content = process_api_response(textract_response)

        s3_resource = boto3.resource('s3')
        CsvBuilder.save_csv_to_s3(csv_content,
            s3_resource=s3_resource, 
            bucket_name=S3_BUCKET_FOR_CSV,
            file_name='{0}.csv'.format(s3_object_name)
        )

        message = '[SUCCESS] Successfully detect document\'s text.'
        
    print(message)
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }


if __name__ == '__main__':
    csv_content = process_api_response(SAMPLE_API_RESPONSE)
    CsvBuilder.save_csv_to_local(csv_content, 'temp.csv')
