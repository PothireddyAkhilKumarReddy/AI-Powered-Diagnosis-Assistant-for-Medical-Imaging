# Testing Guide - All 36 Issues Resolved

## Quick Start

### 1. Start the Backend
```bash
cd backend
python app_simple.py
# Server runs on http://localhost:5003
```

## API Testing Examples

### Health Check
```bash
curl http://localhost:5003/api/health | python -m json.tool
```

### Authentication Tests

#### Signup (Valid)
```bash
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "fullName": "John Doe",
    "phone": "+1234567890"
  }'
```

#### Signup - Invalid Email
```bash
# Should fail with INVALID_EMAIL code
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "notanemail",
    "password": "SecurePassword123!",
    "fullName": "John Doe"
  }'
```

#### Signup - Weak Password
```bash
# Should fail with WEAK_PASSWORD code
# Valid password must have: 8+ chars, uppercase, digit, special char
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "weak",
    "fullName": "John Doe"
  }'
```

#### Signup - Invalid Phone
```bash
# Should fail with INVALID_PHONE code
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "fullName": "John Doe",
    "phone": "invalid"
  }'
```

#### Signup - Duplicate Email
```bash
# Should fail with EMAIL_ALREADY_EXISTS code (409 Conflict)
# First signup succeeds, second fails
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "duplicate@example.com",
    "password": "SecurePassword123!",
    "fullName": "John Doe"
  }'

# Second attempt with same email
curl -X POST http://localhost:5003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "duplicate@example.com",
    "password": "SecurePassword123!",
    "fullName": "John Doe"
  }'
```

#### Login (Valid)
```bash
curl -X POST http://localhost:5003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
# Returns: { "token": "uuid-here", "user": {...} }
```

#### Login - Invalid Credentials
```bash
curl -X POST http://localhost:5003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "WrongPassword123!"
  }'
# Returns: 401 INVALID_CREDENTIALS
```

#### Verify Token
```bash
TOKEN="your-token-from-login"
curl http://localhost:5003/api/auth/verify \
  -H "Authorization: Bearer $TOKEN"
```

#### Logout
```bash
TOKEN="your-token-from-login"
curl -X POST http://localhost:5003/api/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

### Chat Testing

#### Valid Chat Message
```bash
curl -X POST http://localhost:5003/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is COVID-19?"
  }'
```

#### Empty Message (Should fail)
```bash
curl -X POST http://localhost:5003/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": ""
  }'
# Returns: 400 EMPTY_MESSAGE
```

#### Message Too Long (Should fail)
```bash
curl -X POST http://localhost:5003/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "'$(python -c 'print("x" * 5001)')'"
  }'
# Returns: 413 MESSAGE_TOO_LONG
```

### Predict Testing

#### Valid File Upload
```bash
curl -X POST http://localhost:5003/api/predict \
  -F "image=@/path/to/image.jpg"
```

#### Invalid File Type
```bash
# Create a text file
echo "not an image" > test.txt
curl -X POST http://localhost:5003/api/predict \
  -F "image=@test.txt"
# Returns: 400 INVALID_FILE_TYPE
```

#### File Too Large
```bash
# Create a file larger than 10MB
dd if=/dev/zero of=large.jpg bs=1M count=11
curl -X POST http://localhost:5003/api/predict \
  -F "image=@large.jpg"
# Returns: 413 FILE_TOO_LARGE
```

### Rate Limiting Tests

#### Exceeding Rate Limit
```bash
# Signup endpoint: 50/hour limit
for i in {1..51}; do
  curl -X POST http://localhost:5003/api/auth/signup \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"test$i@example.com\", \"password\": \"SecurePassword123!\", \"fullName\": \"User $i\"}" &
done
wait
# 51st request returns: 429 RATE_LIMIT_EXCEEDED
```

## Error Response Format

All endpoints return consistent format:

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "code": "SUCCESS_CODE",
  "user": {},
  "token": "..."
}
```

### Error Response
```json
{
  "success": false,
  "error": "Human readable error message",
  "code": "ERROR_CODE",
  "field": "field_name"  // optional
}
```

## Error Codes Reference

### Authentication Errors
- `MISSING_FIELDS` - 400: Required fields missing
- `INVALID_EMAIL` - 400: Email format invalid
- `WEAK_PASSWORD` - 400: Password doesn't meet requirements
- `INVALID_PHONE` - 400: Phone format invalid
- `INVALID_NAME` - 400: Name contains invalid characters
- `EMAIL_ALREADY_EXISTS` - 409: Email already registered
- `INVALID_CREDENTIALS` - 401: Wrong email or password
- `NO_TOKEN` - 401: Token missing
- `INVALID_TOKEN` - 401: Token invalid
- `TOKEN_EXPIRED` - 401: Token has expired

### File Upload Errors
- `NO_IMAGE` - 400: No file provided
- `NO_FILE_SELECTED` - 400: Empty filename
- `INVALID_FILE_TYPE` - 400: File type not allowed
- `FILE_TOO_LARGE` - 413: File exceeds 10MB
- `PROCESSING_ERROR` - 500: Error processing file

### Chat Errors
- `INVALID_REQUEST` - 400: Invalid JSON body
- `EMPTY_MESSAGE` - 400: Message is empty
- `MESSAGE_TOO_LONG` - 413: Message exceeds 5000 chars

### Rate Limiting
- `RATE_LIMIT_EXCEEDED` - 429: Too many requests

### Server Errors
- `SERVER_ERROR` - 500: Internal server error
- `NOT_FOUND` - 404: Endpoint not found
- `METHOD_NOT_ALLOWED` - 405: HTTP method not allowed
- `BAD_REQUEST` - 400: Invalid request

## Password Requirements

For signup, password must contain:
1. ✓ At least 8 characters
2. ✓ At least one uppercase letter (A-Z)
3. ✓ At least one digit (0-9)
4. ✓ At least one special character (!@#$%^&*()_+-=[]{};;:'"<>?/\|`~)

### Valid Passwords
- `SecurePass123!`
- `MyP@ssw0rd`
- `Test123!@#`

### Invalid Passwords
- `password123` - No uppercase or special char
- `PASSWORD!` - No digit
- `Pass123` - No special char
- `Short1!` - Too short

## File Upload Requirements

Allowed formats: jpg, jpeg, png, gif
- Maximum size: 10MB
- Filenames are sanitized and timestamped
- Files saved in `uploads/` directory

## Rate Limits

Endpoint limits (per IP address, per hour):
- `/api/auth/signup` - 50 requests/hour
- `/api/auth/login` - 50 requests/hour
- `/api/predict` - 20 requests/hour
- `/api/chat` - 100 requests/hour

## Configuration

See `.env` file for configuration:
```
GEMINI_API_KEY=your-api-key
FLASK_ENV=development
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif
TOKEN_EXPIRY_DAYS=7
PASSWORD_MIN_LENGTH=8
RATE_LIMIT_AUTH=50/hour
RATE_LIMIT_PREDICT=20/hour
RATE_LIMIT_CHAT=100/hour
```

## Troubleshooting

### Backend won't start
1. Check Python 3 is installed: `python --version`
2. Check Flask is installed: `pip install flask`
3. Check port 5003 is not in use: `lsof -i :5003`

### Import errors
1. Install requirements: `pip install -r requirements.txt`
2. Check Python path: `which python`

### Token validation fails
1. Ensure token hasn't expired (7 days)
2. Ensure token format is: `Authorization: Bearer <token>`
3. Use exact token from login response

---
**All 36 Issues Resolved** ✓ Complete testing guide available
