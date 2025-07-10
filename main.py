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

# Pydantic models
class DeleteRequest(BaseModel):
    """Model for SQS message deletion request"""
    id_aws: str = Field(..., description="AWS account ID (e.g.: 097826606700)")
    queue_name: str = Field(..., description="Queue name (e.g.: DLQ-PROD-ActiveCampaign.fifo)")
    sqs_endpoint: str = Field(..., description="SQS endpoint (e.g.: sqs.us-east-2.amazonaws.com)")
    receipt_handle: str = Field(..., description="Message receipt handle")

class DeleteResponse(BaseModel):
    """Model for deletion response"""
    success: bool
    message: str
    queue_url: Optional[str] = None
    
class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    service: str
    version: str

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("API_TITLE", "AWS SQS Delete Service"),
    version=os.getenv("API_VERSION", "1.0.2"),
    description=os.getenv("API_DESCRIPTION", "API to delete messages from Amazon SQS"),
    docs_url="/docs",
    redoc_url="/redoc"
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

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint - NO authentication"""
    return HealthResponse(
        status="online",
        service="AWS SQS Delete Service",
        version=os.getenv("API_VERSION", "1.0.0")
    )

@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check endpoint - NO authentication"""
    return HealthResponse(
        status="healthy",
        service="AWS SQS Delete Service",
        version=os.getenv("API_VERSION", "1.0.0")
    )

@app.post("/delete", response_model=DeleteResponse)
async def delete_message(request: DeleteRequest, _: bool = Depends(verify_api_key)):
    """
    Delete a message from SQS using the receipt handle
    
    **REQUIRES AUTHENTICATION**: Use header X-API-Key: your_password
    
    Args:
        request: Request data containing message information
        
    Returns:
        DeleteResponse: Response with operation status
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

@app.get("/test-connection")
async def test_connection(_: bool = Depends(verify_api_key)):
    """
    Test connection with AWS SQS
    
    **REQUIRES AUTHENTICATION**: Use header X-API-Key: your_password
    """
    try:
        sqs = get_sqs_client()
        # Try to list queues to test connection
        response = sqs.list_queues(MaxResults=1)
        return {
            "success": True,
            "message": "AWS SQS connection established successfully",
            "region": os.getenv('AWS_DEFAULT_REGION', 'us-east-2')
        }
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to AWS SQS: {str(e)}"
        ) 