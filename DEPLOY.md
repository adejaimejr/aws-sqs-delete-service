# 🚀 Simplified Deploy - AWS SQS Delete Service

**[🇧🇷 Versão em Português](DEPLOY-PT.md)**

## ⚡ Deploy in One Command

```bash
./deploy.sh
```

This single script does **EVERYTHING**:
- ✅ Automatic versioning
- ✅ Docker image build
- ✅ Push to Docker Hub
- ✅ Generates stack-production.yaml automatically (using variables)
- ✅ Provides server commands
- ✅ **Fully configurable via .env**

## ⚙️ Configuration (Optional)

### 1. Create Configuration File
```bash
# Copy example
cp config.env.example .env

# Edit settings
nano .env
```

### 2. Main Variables
```bash
# Deploy
SERVICE_NAME=aws-sqs-delete
DOMAIN=sqs-api.example.com
NETWORK_NAME=network_swarm_public
LOGS_VOLUME_PATH=/opt/docker/logs/aws-sqs
DOCKER_IMAGE=your-registry/aws-sqs-remove

# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-2

# API
API_PASSWORD=your_api_password
```

## 🎯 How to Use

### 1. Run the Script
```bash
./deploy.sh
```

### 2. Choose Version Type
```
1) Patch (1.0.1 → 1.0.2) - Bug fixes
2) Minor (1.0.1 → 1.1.0) - New features  
3) Major (1.0.1 → 2.0.0) - Breaking changes
4) Custom - Define version manually
```

### 3. Confirm Build
The script shows the new version and asks for confirmation.

### 4. Wait for Build
Automatic multi-architecture build (AMD64 + ARM64).

### 5. Use Commands on Server
The script provides ready commands to execute on the server.

## 📁 Generated Files

- **`VERSION`** - Updated automatically
- **`stack-production.yaml`** - Generated with new version

## 🖥️ Server Commands

```bash
# Remove current stack
docker stack rm aws-sqs-delete

# Wait for cleanup
sleep 15

# Pull new image
docker pull your-registry/aws-sqs-remove:X.X.X

# Deploy new stack
docker stack deploy -c stack-production.yaml aws-sqs-delete

# Verify
docker service ls | grep aws-sqs-delete
curl -k https://your-domain.com/health
```

## ✨ Advantages

- **Simplicity**: Single script for everything
- **Automation**: Zero manual configuration
- **Versioning**: Semantic and automatic
- **Template**: Stack generated dynamically with variables
- **Flexibility**: Fully configurable via .env
- **Reusability**: Same script for different environments
- **Security**: Credentials in separate file

## 🎉 Result

At the end, you'll have:
- ✅ Versioned Docker image on Docker Hub
- ✅ Updated production stack (with your configurations)
- ✅ Ready commands for server
- ✅ Controlled versioning
- ✅ **Fully configurable and reusable project**

## 🔄 Different Environments

```bash
# Development
cp config.env.example .env.dev
# Edit .env.dev
cp .env.dev .env && ./deploy.sh

# Production  
cp config.env.example .env.prod
# Edit .env.prod
cp .env.prod .env && ./deploy.sh
``` 