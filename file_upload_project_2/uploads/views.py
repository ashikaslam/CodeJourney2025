import boto3
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            # Get the uploaded file from the request
            file = request.FILES['file']

            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME,
            )

            # Specify the path inside the bucket
            file_path = f"upload_test/{file.name}"

            # Upload the file to the specified path in the S3 bucket
            print("hello come>>>")
            s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_path)
            print("hello done")

            return JsonResponse({'message': 'File uploaded successfully!', 'path': file_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'upload.html')





'''


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload with Progress Bar</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for the progress bar */
        .progress-bar {
            transition: width 0.3s ease;
        }
    </style>
</head>
<body class="bg-gray-100 font-sans">

    <div class="max-w-xl mx-auto my-10 p-6 bg-white shadow-lg rounded-lg">
        <h1 class="text-2xl font-semibold text-center text-gray-800">Upload File to S3</h1>
        
        <!-- Form with CSRF token -->
        <form id="upload-form" class="mt-6" method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <input type="file" id="file" name="file" class="w-full py-2 px-3 border border-gray-300 rounded-md" required><br><br>
            <button type="submit" class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors">Upload</button>
        </form>

        <!-- Progress Bar Section -->
        <div class="mt-6">
            <label class="text-gray-700">Uploading and Processing</label>
            <div class="w-full bg-gray-200 rounded-md h-2 mt-2">
                <div class="progress-bar bg-blue-500 h-2 rounded-md" id="upload-progress" style="width: 0%;"></div>
            </div>
            <p id="upload-status" class="text-sm text-gray-600 mt-2">Not started</p>
        </div>
    </div>

    <!-- JavaScript -->
    <script>
        const form = document.getElementById('upload-form');
        const uploadProgress = document.getElementById('upload-progress');
        const uploadStatus = document.getElementById('upload-status');

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const fileInput = document.getElementById('file');
            const file = fileInput.files[0];

            if (!file) {
                alert('Please select a file first.');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            // AJAX request to Django view
            const xhr = new XMLHttpRequest();

            // Django endpoint URL
            xhr.open('POST', '/upload/', true);

            // Add CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            // Track upload progress
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 80; // 80% for upload
                    uploadProgress.style.width = percentComplete + '%';
                    uploadStatus.textContent = `Uploading: ${Math.round(percentComplete)}%`;
                }
            };

            // Handle success or failure
            xhr.onload = () => {
                if (xhr.status === 200) {
                    uploadProgress.style.width = '80%'; // Upload phase complete
                    uploadStatus.textContent = 'Upload to Server Complete!';

                    // Simulate processing to S3
                    let processingPercent = 80; // Start from 80%
                    const processingInterval = setInterval(() => {
                        if (processingPercent < 100) {
                            processingPercent += 2; // Simulate S3 processing
                            uploadProgress.style.width = processingPercent + '%';
                            uploadStatus.textContent = `Uploading and Processing: ${processingPercent}%`;
                        } else {
                            clearInterval(processingInterval);
                            uploadStatus.textContent = 'Upload and Processing Complete!';
                        }
                    }, 100); // Adjust speed of processing here
                } else {
                    uploadStatus.textContent = 'Upload failed. Please try again.';
                }
            };

            xhr.onerror = () => {
                uploadStatus.textContent = 'Error occurred while uploading. Please try again.';
            };

            // Send the file to the server
            xhr.send(formData);
        });
    </script>

</body>
</html>




'''
