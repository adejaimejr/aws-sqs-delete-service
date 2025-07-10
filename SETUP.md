# ⚡ Quick Setup - AWS SQS Delete Service

**[🇧🇷 Versão em Português](SETUP-PT.md)**

## 🚀 Standard Deploy (no configuration)

```bash
# Clone the project
git clone https://github.com/adejaimejr/aws-sqs-delete-service.git
cd aws-sqs-delete-service

# Direct deploy (uses default settings)
./deploy.sh
```

## ⚙️ Custom Deploy (with configuration)

### 1. Copy Template
```bash
cp config.env.example .env
```

### 2. Edit Configuration
```bash
nano .env
```

**Example of custom .env:**
```bash
# Common customizations
SERVICE_NAME=my-sqs-service
DOMAIN=sqs.mydomain.com
NETWORK_NAME=my_swarm_network
LOGS_VOLUME_PATH=/opt/logs/sqs

# Specific credentials
AWS_ACCESS_KEY_ID=AKIA_YOUR_KEY
AWS_SECRET_ACCESS_KEY=Your_Secret_Key
API_PASSWORD=my_password_123
```

### 3. Deploy
```bash
./deploy.sh
```

## 🌍 Multiple Environments

### Development
```bash
cp config.env.example .env.dev
# Edit .env.dev with dev configs
cp .env.dev .env && ./deploy.sh
```

### Production
```bash
cp config.env.example .env.prod
# Edit .env.prod with prod configs
cp .env.prod .env && ./deploy.sh
```

### Staging
```bash
cp config.env.example .env.staging
# Edit .env.staging
cp .env.staging .env && ./deploy.sh
```

## 🔧 Important Configurations

### For Different Servers
```bash
# Server 1
NODE_HOSTNAME=server-01
LOGS_VOLUME_PATH=/mnt/disk1/logs/sqs

# Server 2  
NODE_HOSTNAME=server-02
LOGS_VOLUME_PATH=/mnt/disk2/logs/sqs
```

### For Different Domains
```bash
# Development
DOMAIN=sqs-dev.company.com

# Production
DOMAIN=sqs.company.com

# Specific client
DOMAIN=sqs-client1.company.com
```

### For Different Resources
```bash
# Small environment
CPU_LIMIT=0.5
MEMORY_LIMIT=512M

# Robust environment
CPU_LIMIT=2
MEMORY_LIMIT=2048M
```

## ✅ Advantages

- **Flexible**: Reuses the same code for N environments
- **Secure**: Credentials in separate file (not versioned)
- **Simple**: One command does everything
- **Versioned**: Automatic version control
- **Professional**: Dynamically generated stack

## 🎯 Result

Regardless of configuration, you'll always have:
- ✅ Versioned Docker image
- ✅ Custom generated stack
- ✅ Ready commands for server
- ✅ Reproducible deployment 