# File Upload Unittest

Testing file uploads with Django REST Framework (DRF) requires
creating temporary files and simulating multipart form data. Here's how to do it properly:

## Basic File Upload Test

```python
import tempfile
from PIL import Image
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class FileUploadTests(APITestCase):
    def setUp(self):
        # Create a user and get authentication token if needed
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
    def test_image_upload(self):
        # Create a temporary image file
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        
        # Upload the file
        url = reverse('upload-image')
        data = {'image': tmp_file}
        response = self.client.post(url, data, format='multipart')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('image_url' in response.data)
        
        # Clean up
        tmp_file.close()
```

## Testing Different File Types

For non-image files:

```python
def test_document_upload(self):
    # Create a temporary text file
    tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
    tmp_file.write(b'This is a test document')
    tmp_file.seek(0)
    
    url = reverse('upload-document')
    data = {'document': tmp_file}
    response = self.client.post(url, data, format='multipart')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    tmp_file.close()
```

## Testing JWT Authentication with File Upload

```python
def test_authenticated_file_upload(self):
    # Get JWT token
    token_url = reverse('token_obtain_pair')
    token_response = self.client.post(
        token_url, 
        {'username': 'testuser', 'password': 'testpassword'}, 
        format='json'
    )
    token = token_response.data['access']
    
    # Create file
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    Image.new('RGB', (100, 100)).save(tmp_file)
    tmp_file.seek(0)
    
    # Upload with authentication
    url = reverse('upload-image')
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    data = {'image': tmp_file}
    response = self.client.post(url, data, format='multipart')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    tmp_file.close()
```

## Testing File Validation

```python
def test_file_size_validation(self):
    # Create a large file
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    large_image = Image.new('RGB', (2000, 2000))
    large_image.save(tmp_file, quality=100)
    tmp_file.seek(0)
    
    url = reverse('upload-image')
    data = {'image': tmp_file}
    response = self.client.post(url, data, format='multipart')
    
    # Expecting validation error
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('File too large', str(response.data))
    tmp_file.close()
```

## Testing Multiple File Uploads

```python
def test_multiple_file_upload(self):
    # Create multiple files
    files = []
    for i in range(3):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        Image.new('RGB', (100, 100)).save(tmp_file)
        tmp_file.seek(0)
        files.append(tmp_file)
    
    url = reverse('upload-multiple')
    data = {'files': files}
    response = self.client.post(url, data, format='multipart')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(response.data['files']), 3)
    
    # Clean up
    for file in files:
        file.close()
```

Remember that in real tests, you'll need to clean up any files that get saved
to your storage system during tests to prevent accumulation of test files.
