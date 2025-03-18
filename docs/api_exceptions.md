Django REST Framework's `APIException` is a powerful base exception class that provides standardized error handling for API views. Here are the key features of `APIException`:

## Core Features of APIException

### 1. Default Attributes
- `status_code`: HTTP status code (defaults to 500)
- `default_detail`: Default error message
- `default_code`: Default error code for API documentation

### 2. Customization
```python
class CustomAPIException(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'forbidden'
```

### 3. Runtime Customization
```python
# Raise with custom message
raise APIException(detail="Custom error message")

# Raise with custom message and code
raise APIException(detail="Custom error message", code="custom_code")
```

### 4. Built-in Error Rendering
- Automatically converts to appropriate response format (JSON/XML)
- Includes status code, detail message, and code
- Handles internationalization with Django's translation system

### 5. Built-in Exception Subclasses
DRF provides many specialized subclasses:
- `ParseError` (400) - Malformed request
- `AuthenticationFailed` (401) - Invalid authentication
- `NotAuthenticated` (401) - Authentication required
- `PermissionDenied` (403) - Authenticated but not authorized
- `NotFound` (404) - Requested resource not found
- `MethodNotAllowed` (405) - HTTP method not supported
- `ValidationError` (400) - Failed input validation
- `Throttled` (429) - Request rate limit exceeded

### 6. Exception Handler Integration
```python
# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
}
```

### 7. Custom Exception Handling
```python
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Now add custom error details
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error_type'] = exc.__class__.__name__
        
    return response
```

### 8. Error Response Format
Default JSON response format:
```json
{
    "detail": "Error message here"
}
```

With customized handler, you could have:
```json
{
    "detail": "Error message here",
    "status_code": 400,
    "error_type": "ValidationError",
    "errors": [...]
}
```

These features make `APIException` a flexible foundation for creating consistent error responses across your API.
