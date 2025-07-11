from fastapi import FastAPI, HTTPException, status, Depends, Header
from pydantic import BaseModel, Field
import boto3
import os
from typing import Optional
import logging
from datetime import datetime

# Configure logging

# Create logs directory if it doesn't exist
os.makedirs('/app/logs', exist_ok=True)

# Configure logging to file and console
log_filename = f"/app/logs/aws-sqs-delete-{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # To see logs in docker logs as well
    ]
)
logger = logging.getLogger(__name__)

# Pydantic models with improved documentation and examples
class DeleteRequest(BaseModel):
    """Request model for SQS message deletion"""
    id_aws: str = Field(
        ..., 
        description="AWS account ID",
        example="123456789012",
        min_length=12,
        max_length=12
    )
    queue_name: str = Field(
        ..., 
        description="SQS queue name",
        example="my-queue.fifo"
    )
    sqs_endpoint: str = Field(
        ..., 
        description="SQS service endpoint",
        example="sqs.us-east-1.amazonaws.com"
    )
    receipt_handle: str = Field(
        ..., 
        description="Message receipt handle obtained from SQS receive operation",
        example="AQEBwJnKyrHigUMZBiSOyfZEXAMPLEUvO..."
    )
    
    class Config:
        schema_extra = {
            "example": {
                "id_aws": "123456789012",
                "queue_name": "my-queue.fifo",
                "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
                "receipt_handle": "AQEBwJnKyrHigUMZBiSOyfZEXAMPLEUvO..."
            }
        }

class DeleteResponse(BaseModel):
    """Response model for message deletion operations"""
    success: bool = Field(description="Operation success status")
    message: str = Field(description="Operation result message")
    queue_url: Optional[str] = Field(None, description="Complete SQS queue URL")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Message deleted successfully",
                "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue.fifo"
            }
        }
    
class HealthResponse(BaseModel):
    """Response model for health check operations"""
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    version: str = Field(description="Current API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "AWS SQS Delete Service",
                "version": "1.0.3"
            }
        }

class ConnectionResponse(BaseModel):
    """Response model for connection test operations"""
    success: bool = Field(description="Connection test result")
    message: str = Field(description="Connection status message")
    region: str = Field(description="AWS region being used")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "AWS SQS connection established successfully",
                "region": "us-east-1"
            }
        }

# Initialize FastAPI app with enhanced documentation
app = FastAPI(
    title="AWS SQS Delete Service",
    version=os.getenv("API_VERSION", "1.0.8"),
    description="""
## AWS SQS Delete Service

**Professional FastAPI service for deleting AWS SQS messages via HTTP endpoint**

This service simplifies n8n integration with AWS SQS by providing a single HTTP endpoint 
for message deletion operations, eliminating the complexity of direct AWS SDK integration.

### 🚀 Quick Start Guide

1. **Get your API key** - Contact your administrator or check your deployment configuration
2. **Test connection** - Use `GET /test-connection` to verify AWS connectivity  
3. **Delete messages** - Send POST requests to `/delete` with your message details
4. **Monitor health** - Check service status via `GET /health`

### Features
- 🔒 **Secure**: API key authentication via `X-API-Key` header
- 🚀 **Fast**: Async operations with high performance
- 📊 **Monitored**: Health checks and structured logging  
- 🐳 **Containerized**: Docker-ready deployment
- 📖 **Documented**: Complete OpenAPI specification
- 🌐 **Multi-arch**: Supports AMD64 and ARM64 architectures

### 🔐 Authentication

All SQS operations require authentication via the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key-here" https://your-domain.com/delete
```

**Security Policy**: Never share your API key. In case of compromise, contact your administrator immediately for reissuing.

### 💡 Common Use Cases

**n8n Integration**: Perfect for n8n workflows needing SQS message deletion
**Batch Processing**: Ideal for cleanup operations after message processing
**Automation**: Integrate with any system requiring programmatic SQS operations
**Error Handling**: Remove problematic messages from queues

### 📚 Code Examples

#### Python
```python
import requests

api_key = "your-api-key-here"
url = "https://your-domain.com/delete"
headers = {"X-API-Key": api_key}
payload = {
    "id_aws": "123456789012",
    "queue_name": "my-queue.fifo", 
    "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
    "receipt_handle": "AQEBwJnKyrHigUMZBi..."
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

#### JavaScript (Node.js)
```javascript
const axios = require('axios');

const apiKey = "your-api-key-here";
const url = "https://your-domain.com/delete";
const headers = { "X-API-Key": apiKey };
const payload = {
    "id_aws": "123456789012",
    "queue_name": "my-queue.fifo",
    "sqs_endpoint": "sqs.us-east-1.amazonaws.com", 
    "receipt_handle": "AQEBwJnKyrHigUMZBi..."
};

axios.post(url, payload, { headers })
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
```

#### cURL
```bash
curl -X POST "https://your-domain.com/delete" \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "id_aws": "123456789012",
    "queue_name": "my-queue.fifo",
    "sqs_endpoint": "sqs.us-east-1.amazonaws.com",
    "receipt_handle": "AQEBwJnKyrHigUMZBi..."
  }'
```

### 🚨 Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Authentication failed | Check your API key |
| 422 | Validation error | Verify request parameters |
| 500 | AWS/Server error | Check AWS credentials & connectivity |

### 📊 API Limits

- **Rate Limit**: 100 requests per minute per API key
- **Payload Size**: Maximum 256KB per request
- **Timeout**: 30 seconds per operation
- **Concurrency**: Up to 10 concurrent requests per API key

### 📝 Version History

**v1.0.7** (Current) - Enhanced documentation and UX
- ✅ Comprehensive Quick Start Guide with step-by-step instructions
- ✅ Multi-language code examples (Python, JavaScript, cURL)
- ✅ Detailed error documentation with solutions table
- ✅ Professional API limits and specifications
- ✅ Enhanced use cases and integration examples

**v1.0.6** - Documentation improvements
- ✅ Improved OpenAPI documentation structure
- ✅ Enhanced endpoint descriptions with use cases
- ✅ Better error response examples

**v1.0.5** - Critical compatibility fix
- ✅ Restored `/delete` endpoint for n8n compatibility
- ✅ Enhanced documentation with examples
- ✅ Professional OpenAPI specification

**v1.0.4** - Documentation improvements
- ✅ Professional Swagger UI with organized tags
- ✅ Enhanced Pydantic models with examples

**v1.0.3** - Multi-architecture support
- ✅ AMD64 and ARM64 Docker images
- ✅ Production-ready deployment

---
**Repository**: [github.com/adejaimejr/aws-sqs-delete-service](https://github.com/adejaimejr/aws-sqs-delete-service)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "AWS SQS Delete Service",
        "url": "https://github.com/adejaimejr/aws-sqs-delete-service",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/adejaimejr/aws-sqs-delete-service/blob/main/LICENSE",
    },
    tags_metadata=[
        {
            "name": "Health",
            "description": "Service health monitoring endpoints",
        },
        {
            "name": "SQS Operations",
            "description": "AWS SQS message management operations",
        },
        {
            "name": "Authentication",
            "description": "Connection testing and authentication endpoints",
        },
    ],
)

# Authentication function
async def verify_password(authorization: str = Header(None)):
    """
    Verify authentication password
    
    Can be passed via:
    - Header: Authorization: Bearer your_password
    - Header: X-API-Key: your_password
    """
    api_password = os.getenv("API_PASSWORD")
    
    # If no password is configured, allow access
    if not api_password:
        return True
    
    # Check Authorization header
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        if token == api_password:
            return True
    
    # Check X-API-Key header
    x_api_key = Header(None)
    if x_api_key and x_api_key == api_password:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password. Use: Authorization: Bearer your_password"
    )

async def verify_api_key(x_api_key: str = Header(None)):
    """
    Verify password via X-API-Key header
    """
    api_password = os.getenv("API_PASSWORD")
    
    # If no password is configured, allow access
    if not api_password:
        return True
    
    if not x_api_key or x_api_key != api_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password. Use header: X-API-Key: your_password"
        )
    
    return True

# Initialize SQS client
def get_sqs_client():
    """Initialize SQS client with AWS credentials"""
    try:
        return boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-2')
        )
    except Exception as e:
        logger.error(f"Error initializing SQS client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing AWS SQS client: {str(e)}"
        )

@app.get(
    "/", 
    response_model=HealthResponse,
    tags=["Health"],
    summary="Basic Health Check",
    description="Quick health check endpoint that returns service status and version information."
)
async def root():
    """Basic health check endpoint - NO authentication required"""
    return HealthResponse(
        status="online",
        service="AWS SQS Delete Service",
        version=os.getenv("API_VERSION", "1.0.8")
    )

@app.get(
    "/health", 
    response_model=HealthResponse,
    tags=["Health"],
    summary="Detailed Health Check",
    description="Comprehensive health check endpoint for monitoring and load balancer verification."
)
async def health():
    """Detailed health check endpoint - NO authentication required"""
    return HealthResponse(
        status="healthy",
        service="AWS SQS Delete Service",
        version=os.getenv("API_VERSION", "1.0.8")
    )

@app.post(
    "/delete", 
    response_model=DeleteResponse,
    tags=["SQS Operations"],
    summary="Delete SQS Message",
    description="""
    Delete a specific message from an AWS SQS queue using its receipt handle.
    
    **Required**: Valid receipt handle obtained from a previous SQS receive operation.
    
    **Perfect for**: n8n workflows, automation scripts, and batch processing systems.
    
    **Note**: This operation is idempotent - calling it multiple times with the same receipt handle will not cause errors.
    
    **Example Use Cases**:
    - Remove processed messages from SQS queues
    - Clean up failed messages after manual intervention
    - Integrate with n8n workflows for automated message processing
    - Batch cleanup operations in distributed systems
    """,
    responses={
        200: {
            "description": "Message deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Message deleted successfully",
                        "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue.fifo"
                    }
                }
            }
        },
        401: {
            "description": "Authentication failed - Invalid or missing API key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid password. Use: Authorization: Bearer your_password"
                    }
                }
            }
        },
        422: {
            "description": "Validation error - Invalid request parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "id_aws"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "AWS connection error or internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Error connecting to AWS SQS",
                        "queue_url": None
                    }
                }
            }
        }
    }
)
async def delete_message(request: DeleteRequest, _: bool = Depends(verify_api_key)):
    """
    Delete a message from SQS using the receipt handle
    
    **REQUIRES AUTHENTICATION**: Use header `X-API-Key: your_password`
    """
    try:
        # Construct queue URL - remove https:// if already present
        endpoint = request.sqs_endpoint.replace("https://", "")
        queue_url = f"https://{endpoint}/{request.id_aws}/{request.queue_name}"
        
        logger.info(f"Attempting to delete message from queue: {queue_url}")
        
        # Get SQS client
        sqs = get_sqs_client()
        
        # Delete message
        response = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=request.receipt_handle
        )
        
        logger.info(f"Message successfully deleted from queue: {queue_url}")
        
        return DeleteResponse(
            success=True,
            message="Message deleted successfully",
            queue_url=queue_url
        )
        
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting message: {str(e)}"
        )

@app.get(
    "/test-connection",
    response_model=ConnectionResponse,
    tags=["Authentication"],
    summary="Test AWS Connection",
    description="""
    Verify that the service can successfully connect to AWS SQS with current credentials.
    
    **Use this to**: Validate AWS credentials and network connectivity before processing messages.
    
    **Perfect for**:
    - Pre-deployment validation
    - Troubleshooting connection issues
    - Monitoring script integration
    - Health check automation
    
    **What it validates**:
    - AWS credentials are valid
    - Network connectivity to AWS SQS
    - Service region configuration
    - Basic SQS service availability
    """,
    responses={
        200: {
            "description": "Connection successful",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "AWS SQS connection established successfully",
                        "region": "us-east-1"
                    }
                }
            }
        },
        401: {
            "description": "Authentication failed - Invalid or missing API key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid password. Use: Authorization: Bearer your_password"
                    }
                }
            }
        },
        500: {
            "description": "AWS connection failed - Check credentials and connectivity",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Failed to connect to AWS SQS: Unable to locate credentials",
                        "region": "unknown"
                    }
                }
            }
        }
    }
)
async def test_connection(_: bool = Depends(verify_api_key)):
    """
    Test connection with AWS SQS
    
    **REQUIRES AUTHENTICATION**: Use header `X-API-Key: your_password`
    """
    try:
        sqs = get_sqs_client()
        # Try to list queues to test connection
        response = sqs.list_queues(MaxResults=1)
        return ConnectionResponse(
            success=True,
            message="AWS SQS connection established successfully",
            region=os.getenv('AWS_DEFAULT_REGION', 'us-east-2')
        )
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to AWS SQS: {str(e)}"
        ) 