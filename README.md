# AWS SQS Delete Service

> **FastAPI service for deleting AWS SQS messages via HTTP endpoint - Perfect for n8n integration**

**[🇧🇷 Versão em Português](README-PT.md)**

## 🚀 Overview

This project was created to **drastically simplify** the use of n8n with AWS SQS, specifically for **removing messages from queues**. Instead of setting up complex integrations or using multiple tools, you can use this service as a simple HTTP endpoint in your n8n workflow.

## 🎯 Problem it Solves

### Without this service:
- Complex AWS credentials configuration in n8n
- Multiple steps for authentication and message removal
- AWS tokens and sessions management
- Repetitive code in workflows

### With this service:
- **A single HTTP endpoint** (`POST /delete`)
- **Centralized configuration** of AWS credentials
- **Instant response** (success/error)
- **Direct integration** with any n8n workflow

## 🛠️ How it Works

This Python service uses **advanced resources** to execute the task:

### Technologies Used:
- **FastAPI** - Modern and fast web framework
- **boto3** - Official AWS SDK for Python
- **asyncio** - Asynchronous programming for high performance
- **Docker** - Containerization for consistent deployment
- **Uvicorn** - High-performance ASGI server

### Architecture:
```
n8n Workflow → HTTP POST → AWS SQS Delete Service → AWS SQS → Response
```

## 🔧 Quick Setup

### 1. Configure environment variables:
```bash
cp config.env.example .env
# Edit .env with your AWS credentials
```

### 2. Run with Docker:
```bash
# Build and Deploy
./deploy.sh

# Or manually
docker build -t aws-sqs-remove .
docker run -p 8000:8000 --env-file .env aws-sqs-remove
```

### 3. Use in n8n:
```json
{
  "method": "POST",
  "url": "http://your-server:8000/delete",
  "headers": {
    "Content-Type": "application/json",
    "X-API-Key": "your-api-key-here"
  },
  "body": {
    "id_aws": "123456789012",
    "queue_name": "your-queue.fifo",
    "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
    "receipt_handle": "AQEBwJ..."
  }
}
```

## 📡 API Endpoints

### `POST /delete`
Remove a specific message from the SQS queue.

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Body:**
```json
{
  "id_aws": "123456789012",
  "queue_name": "your-queue.fifo",
  "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
  "receipt_handle": "AQEBwJ..."
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Message deleted successfully",
  "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/your-queue.fifo"
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "queue_url": null
}
```

### `GET /health`
Check if the service is working.

### `GET /test-connection`
Test AWS SQS connection and validate credentials.

### `GET /docs`
Interactive API documentation (Swagger UI) with comprehensive examples and code snippets.

## 🔒 Security

- **API Key authentication** via `X-API-Key` header
- **AWS credentials** managed via environment variables
- **Input validation** for all parameters
- **Detailed logs** for auditing
- **HTTPS support** when configured with reverse proxy
- **Rate limiting** - 100 requests per minute per API key
- **Secure credential handling** - Never expose sensitive information in logs

## 📁 Project Structure

```
├── main.py              # Main API code
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── deploy.sh           # Automated deployment script
├── config.env.example  # Configuration template
├── SETUP.md           # Detailed setup guide (English)
├── SETUP-PT.md        # Detailed setup guide (Portuguese)
├── DEPLOY.md          # Deployment instructions (English)
├── DEPLOY-PT.md       # Deployment instructions (Portuguese)
└── VERSION            # Version control
```

## 🚀 Advantages for n8n

### Before (Complex):
1. Configure AWS credentials in n8n
2. Create multiple nodes for authentication
3. Manage tokens and sessions
4. Handle errors individually
5. Repeat configuration in each workflow

### Now (Simple):
1. A single HTTP Request node in n8n
2. Standardized endpoint
3. Consistent response
4. Centralized error handling
5. Reusability across all workflows

## 🌟 Advanced Features

- **Async/Await**: Non-blocking operations for high performance
- **Retry Logic**: Automatic attempts on temporary failures
- **Rate Limiting**: Request rate control
- **Health Checks**: Application health monitoring
- **Structured Logging**: Detailed logs for debugging
- **Error Handling**: Robust AWS error handling
- **Professional API Documentation**: Comprehensive Swagger UI with code examples
- **Multi-language Examples**: Python, JavaScript, and cURL examples in documentation
- **Detailed Error Responses**: Structured error messages with solutions
- **Interactive Testing**: Built-in API testing interface via `/docs`

## 🧪 Testing

Test the service with curl:

```bash
# Health check
curl http://localhost:8000/health

# Test AWS connection
curl -H "X-API-Key: your-api-key-here" http://localhost:8000/test-connection

# Delete message
curl -X POST http://localhost:8000/delete \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "id_aws": "123456789012",
    "queue_name": "your-queue.fifo",
    "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
    "receipt_handle": "your-receipt-handle"
  }'
```

## 📖 Additional Documentation

- [SETUP.md](SETUP.md) - Detailed configuration (English)
- [SETUP-PT.md](SETUP-PT.md) - Configuração detalhada (Portuguese)
- [DEPLOY.md](DEPLOY.md) - Deployment instructions (English)
- [DEPLOY-PT.md](DEPLOY-PT.md) - Instruções de deploy (Portuguese)
- [VERSION](VERSION) - Version control

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Share use cases

---

**Developed with ❤️ to simplify the integration between n8n and AWS SQS** 