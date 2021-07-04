import json
import boto3

from models.table_parser import TableParser
from models.form_parser import FormParser
from models.textract import Textract
from models.csv_builder import CsvBuilder
from sample_api_response import SAMPLE_API_RESPONSE
from config import DEFAULT_REGION, S3_BUCKET_FOR_CSV


def process_textract_response(textract_response):
    table_parser = TableParser(textract_response)
    form_parser = FormParser(textract_response)
    return table_parser.get_csv_lines(), form_parser.get_csv_lines()


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
        table_csv_lines, form_csv_lines = process_textract_response(textract_response)

        s3_resource = boto3.resource('s3')
        csv_builder = CsvBuilder(table_csv_lines, form_csv_lines)
        csv_builder.save_csv_to_s3(s3_resource, S3_BUCKET_FOR_CSV, s3_object_name)
        message = '[SUCCESS] Successfully detect document\'s text.'
        
    print(message)
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }


if __name__ == '__main__':
    table_csv_lines, form_csv_lines = process_textract_response(SAMPLE_API_RESPONSE)
    csv_builder = CsvBuilder(table_csv_lines, form_csv_lines)
    csv_builder.save_csv_to_local()
