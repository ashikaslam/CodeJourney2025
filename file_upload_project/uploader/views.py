import boto3
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from botocore.exceptions import ClientError

# Render the HTML upload page
def upload_page(request):
    return render(request, 'uploader/upload.html')

# Handle file upload and stream it to AWS S3
def file_upload_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']  # Get the uploaded file

        # Configure AWS S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Define the S3 bucket and object key
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        object_key = f'uploads/{file.name}'  # Customize path in the bucket

        try:
            # Stream file directly to S3
            s3.upload_fileobj(
                Fileobj=file,
                Bucket=bucket_name,
                Key=object_key,
            )
            # Generate S3 URL
            s3_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_key}'
            return JsonResponse({'message': 'File uploaded successfully!', 's3_url': s3_url}, status=200)
        except ClientError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
