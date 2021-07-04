class Textract:
    def __init__(self, client):
        self.client = client

    def detect_document_text(self, s3_object):
        response = self.client.detect_document_text(
            Document={
                'S3Object': s3_object
            },
        )
        return response

    def analyze_document(self, s3_object):
        response = self.client.analyze_document(
            Document={
                'S3Object': s3_object
            },
            FeatureTypes=[
                'FORMS',
            ],
        )
        return response
