# textractor-from-s3

### What is this?
You should know first that AWS has [Textractor](https://aws.amazon.com/textract/) service, which helps user extract texts from an image. When you call the Textractor API, you will get API response as shown in `sample_api_response1.py` and `sample_api_response2.py`.

Okay, so the objective of this project is to get the text from an image uploaded to an S3 bucket. How does that works?

1. User put an image into S3 bucket.
2. S3 bucket has [Event Notification](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html) on, which will trigger a Lambda function whenever a new image is being put into the bucket.
3. Lambda will call Textractor API, passing the information about a new image uploaded to the S3 bucket.
4. Upon receiving the API response, Lambda will parse that response and generate a CSV file containing the texts.
5. Lambda will store that CSV file onto another S3 bucket.

### Additional Notes
In short, Textractor categorizes the texts detected from an image into some kind of relationships, i.e. `raw`, `form` and `table`.
