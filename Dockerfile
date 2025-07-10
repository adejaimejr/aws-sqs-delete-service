# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create logs directory for production volume mount
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Expose port
EXPOSE 80

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"] 