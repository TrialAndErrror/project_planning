# CORS Troubleshooting Guide

This guide helps you resolve CORS (Cross-Origin Resource Sharing) issues in the Project Planning application.

## 🔍 Quick Diagnosis

### 1. Check CORS Configuration
Run the CORS test script to verify your configuration:
```bash
cd backend
python test_cors.py
```

### 2. Check Browser Console
Open your browser's developer tools and look for CORS errors in the Console tab. Common errors:
- `Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy`
- `No 'Access-Control-Allow-Origin' header is present on the requested resource`

### 3. Check Network Tab
In the Network tab of developer tools, look for:
- Failed requests (red entries)
- Missing CORS headers in response
- Preflight OPTIONS requests failing

## 🛠️ Common Solutions

### Solution 1: Restart Docker Containers
```bash
# Stop containers
docker-compose -f docker-compose.dev.yml down

# Start containers
docker-compose -f docker-compose.dev.yml up --build
```

### Solution 2: Check Environment Variables
Verify the CORS environment variables are set correctly in `docker-compose.dev.yml`:
```yaml
environment:
  - CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000
  - CORS_ALLOW_ALL_ORIGINS=True
```

### Solution 3: Verify Django Settings
Check that `backend/core/settings_dev.py` has:
```python
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000').split(',')
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOW_CREDENTIALS = True
```

### Solution 4: Check Frontend API URL
Verify `frontend/src/stores/auth.js` and `project.js` have the correct API URL:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

And in `docker-compose.dev.yml`:
```yaml
frontend:
  environment:
    - VITE_API_URL=http://localhost:8000
```

## 🧪 Testing CORS

### Test 1: Simple CORS Test
```bash
cd backend
python test_cors.py
```

### Test 2: Manual API Test
```bash
# Test from command line
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://localhost:8000/api/projects/
```

### Test 3: Browser Test
Open browser console and run:
```javascript
fetch('http://localhost:8000/api/projects/', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

## 🚨 Common Issues

### Issue 1: "No 'Access-Control-Allow-Origin' header"
**Cause**: CORS middleware not properly configured or not running
**Solution**: 
- Check that `corsheaders.middleware.CorsMiddleware` is in `MIDDLEWARE` list
- Verify it's placed before `django.middleware.common.CommonMiddleware`
- Restart Django server

### Issue 2: "Credentials not supported"
**Cause**: `CORS_ALLOW_CREDENTIALS` not set to `True`
**Solution**: Ensure `CORS_ALLOW_CREDENTIALS = True` in settings

### Issue 3: "Method not allowed"
**Cause**: CORS methods not properly configured
**Solution**: Check `CORS_ALLOW_METHODS` includes all needed methods

### Issue 4: "Headers not allowed"
**Cause**: CORS headers not properly configured
**Solution**: Check `CORS_ALLOW_HEADERS` includes needed headers like `Authorization`

## 🔧 Advanced Debugging

### Enable CORS Debug Logging
Add to `settings_dev.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'corsheaders': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Check Request Headers
Add a custom middleware to log all requests:
```python
class CORSDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request Origin: {request.META.get('HTTP_ORIGIN')}")
        print(f"Request Method: {request.method}")
        response = self.get_response(request)
        print(f"Response CORS Headers: {dict(response.items())}")
        return response
```

## 📞 Still Having Issues?

1. **Check Docker logs**: `docker-compose -f docker-compose.dev.yml logs backend`
2. **Check Django logs**: Look for CORS-related messages in Django console
3. **Verify ports**: Ensure backend is running on port 8000 and frontend on 3000
4. **Clear browser cache**: Hard refresh (Ctrl+F5) or clear browser cache
5. **Try different browser**: Test in incognito/private mode

## 🎯 Quick Fix Checklist

- [ ] Restart Docker containers
- [ ] Verify environment variables
- [ ] Check Django settings
- [ ] Test with CORS test script
- [ ] Check browser console for errors
- [ ] Verify API URLs match
- [ ] Clear browser cache
- [ ] Test in incognito mode
