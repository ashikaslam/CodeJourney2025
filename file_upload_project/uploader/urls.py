from django.urls import path
from .views import upload_page, file_upload_view

urlpatterns = [
    path('', upload_page, name='upload_page'),  # URL for the upload page
    path('upload/', file_upload_view, name='file_upload'),  # URL for file upload
]
