#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 AWS SQS DELETE - COMPLETE DEPLOY${NC}"
echo "==================================="

# Load configurations from .env file (if exists)
if [ -f ".env" ]; then
    echo -e "${BLUE}📋 Loading configurations from .env...${NC}"
    source .env
else
    echo -e "${YELLOW}⚠️  .env file not found. Using default values.${NC}"
    echo -e "${BLUE}💡 To customize, copy config.env.example to .env${NC}"
fi

# Define default values if not in .env
SERVICE_NAME=${SERVICE_NAME:-aws-sqs-delete}
DOMAIN=${DOMAIN:-sqs-api.example.com}
NETWORK_NAME=${NETWORK_NAME:-network_swarm_public}
LOGS_VOLUME_PATH=${LOGS_VOLUME_PATH:-/opt/docker/logs/aws-sqs}
DOCKER_IMAGE=${DOCKER_IMAGE:-your-registry/aws-sqs-remove}
NODE_HOSTNAME=${NODE_HOSTNAME:-node-01}
CPU_LIMIT=${CPU_LIMIT:-1}
MEMORY_LIMIT=${MEMORY_LIMIT:-1024M}
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-YOUR_AWS_ACCESS_KEY}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-YOUR_AWS_SECRET_KEY}
AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-us-east-1}
API_TITLE=${API_TITLE:-AWS SQS Delete Service}
API_DESCRIPTION=${API_DESCRIPTION:-API to delete messages from Amazon SQS}
API_PASSWORD=${API_PASSWORD:-your_secure_password}
TRAEFIK_ENTRYPOINT=${TRAEFIK_ENTRYPOINT:-websecure}
TRAEFIK_CERT_RESOLVER=${TRAEFIK_CERT_RESOLVER:-letsencryptresolver}
CONTAINER_PORT=${CONTAINER_PORT:-80}

echo -e "${GREEN}✅ Configurations loaded:${NC}"
echo "   • Service: $SERVICE_NAME"
echo "   • Domain: $DOMAIN"
echo "   • Network: $NETWORK_NAME"
echo "   • Image: $DOCKER_IMAGE"

# Function to increment version
increment_version() {
    local version=$1
    local type=${2:-patch}
    
    IFS='.' read -ra VERSION_PARTS <<< "$version"
    major=${VERSION_PARTS[0]}
    minor=${VERSION_PARTS[1]}
    patch=${VERSION_PARTS[2]}
    
    case $type in
        major) echo "$((major + 1)).0.0" ;;
        minor) echo "$major.$((minor + 1)).0" ;;
        patch) echo "$major.$minor.$((patch + 1))" ;;
    esac
}

# Read current version
CURRENT_VERSION=$(cat VERSION 2>/dev/null || echo "1.0.7")
echo -e "${YELLOW}📋 Current version: $CURRENT_VERSION${NC}"

# Choose new version
echo ""
echo "Choose update type:"
echo "1) Patch (bug fix)"
echo "2) Minor (new feature)"
echo "3) Major (breaking change)"
echo "4) Custom"
echo ""
read -p "Option (1-4): " VERSION_TYPE

case $VERSION_TYPE in
    1) NEW_VERSION=$(increment_version $CURRENT_VERSION patch) ;;
    2) NEW_VERSION=$(increment_version $CURRENT_VERSION minor) ;;
    3) NEW_VERSION=$(increment_version $CURRENT_VERSION major) ;;
    4) read -p "Enter new version: " NEW_VERSION ;;
    *) echo -e "${RED}❌ Invalid option${NC}"; exit 1 ;;
esac

echo -e "${GREEN}🎯 New version: $NEW_VERSION${NC}"

# Confirm
read -p "Confirm build and deploy version $NEW_VERSION? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo -e "${YELLOW}❌ Canceled${NC}"
    exit 0
fi

# Update version
echo $NEW_VERSION > VERSION

# Update version in main.py
sed -i '' "s/version=os\.getenv(\"API_VERSION\", \"[^\"]*\")/version=os.getenv(\"API_VERSION\", \"$NEW_VERSION\")/g" main.py

# Build image
echo -e "${BLUE}🔨 Building Docker image v$NEW_VERSION...${NC}"
docker build --platform linux/amd64,linux/arm64 \
    -t $DOCKER_IMAGE:$NEW_VERSION \
    -t $DOCKER_IMAGE:latest \
    --push .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build error${NC}"
    exit 1
fi

# Generate production stack
echo -e "${BLUE}📝 Generating production stack...${NC}"
cat > stack-production.yaml << EOF
version: "3.7"

services:
  $SERVICE_NAME:
    image: $DOCKER_IMAGE:$NEW_VERSION
    networks:
      - $NETWORK_NAME
    volumes:
      - $LOGS_VOLUME_PATH:/app/logs
    environment:
      - AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
      - AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
      - API_TITLE=$API_TITLE
      - API_VERSION=$NEW_VERSION
      - API_DESCRIPTION=$API_DESCRIPTION
      - API_PASSWORD=$API_PASSWORD
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - node.hostname == $NODE_HOSTNAME
      resources:
        limits:
          cpus: "$CPU_LIMIT"
          memory: $MEMORY_LIMIT
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.$SERVICE_NAME.rule=Host(\`$DOMAIN\`)"
        - "traefik.http.routers.$SERVICE_NAME.entrypoints=$TRAEFIK_ENTRYPOINT"
        - "traefik.http.routers.$SERVICE_NAME.tls.certresolver=$TRAEFIK_CERT_RESOLVER"
        - "traefik.http.services.$SERVICE_NAME.loadbalancer.server.port=$CONTAINER_PORT"
        - "traefik.docker.network=$NETWORK_NAME"

volumes:
  aws_sqs_logs:
    external: true
    name: aws_sqs_logs

networks:
  $NETWORK_NAME:
    external: true
    name: $NETWORK_NAME
EOF

echo -e "${GREEN}✅ Build completed!${NC}"
echo ""
echo -e "${BLUE}📋 SERVER COMMANDS:${NC}"
echo "==================="
echo ""
echo -e "${YELLOW}# Copy file to server${NC}"
echo "scp stack-production.yaml user@server:/path/"
echo ""
echo -e "${YELLOW}# Execute on server${NC}"
echo "docker stack rm $SERVICE_NAME"
echo "sleep 15"
echo "docker pull $DOCKER_IMAGE:$NEW_VERSION"
echo "docker stack deploy -c stack-production.yaml $SERVICE_NAME"
echo ""
echo -e "${YELLOW}# Verify${NC}"
echo "docker service ls | grep $SERVICE_NAME"
echo "curl -k https://$DOMAIN/health"
echo ""
echo -e "${GREEN}🎉 Version $NEW_VERSION ready for deploy!${NC}" 