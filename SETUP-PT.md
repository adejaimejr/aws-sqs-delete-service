# ⚡ Setup Rápido - AWS SQS Delete Service

**[🇺🇸 English Version](SETUP.md)**

## 🚀 Deploy Padrão (sem configuração)

```bash
# Clone o projeto
git clone https://github.com/adejaimejr/aws-sqs-delete-service.git
cd aws-sqs-delete-service

# Deploy direto (usa configurações padrão)
./deploy.sh
```

## ⚙️ Deploy Personalizado (com configuração)

### 1. Copiar Template
```bash
cp config.env.example .env
```

### 2. Editar Configurações
```bash
nano .env
```

**Exemplo de .env personalizado:**
```bash
# Customizações mais comuns
SERVICE_NAME=meu-sqs-service
DOMAIN=sqs.meudominio.com.br
NETWORK_NAME=minha_rede_swarm
LOGS_VOLUME_PATH=/opt/logs/sqs

# Credenciais específicas
AWS_ACCESS_KEY_ID=AKIA_SUA_KEY
AWS_SECRET_ACCESS_KEY=Sua_Secret_Key
API_PASSWORD=minha_senha_123
```

### 3. Deploy
```bash
./deploy.sh
```

## 🌍 Múltiplos Ambientes

### Desenvolvimento
```bash
cp config.env.example .env.dev
# Editar .env.dev com configs de dev
cp .env.dev .env && ./deploy.sh
```

### Produção
```bash
cp config.env.example .env.prod
# Editar .env.prod com configs de prod
cp .env.prod .env && ./deploy.sh
```

### Staging
```bash
cp config.env.example .env.staging
# Editar .env.staging
cp .env.staging .env && ./deploy.sh
```

## 🔧 Configurações Importantes

### Para Diferentes Servidores
```bash
# Servidor 1
NODE_HOSTNAME=servidor-01
LOGS_VOLUME_PATH=/mnt/disk1/logs/sqs

# Servidor 2  
NODE_HOSTNAME=servidor-02
LOGS_VOLUME_PATH=/mnt/disk2/logs/sqs
```

### Para Diferentes Domínios
```bash
# Desenvolvimento
DOMAIN=sqs-dev.empresa.com.br

# Produção
DOMAIN=sqs.empresa.com.br

# Cliente específico
DOMAIN=sqs-cliente1.empresa.com.br
```

### Para Diferentes Recursos
```bash
# Ambiente pequeno
CPU_LIMIT=0.5
MEMORY_LIMIT=512M

# Ambiente robusto
CPU_LIMIT=2
MEMORY_LIMIT=2048M
```

## ✅ Vantagens

- **Flexível**: Reutiliza o mesmo código para N ambientes
- **Seguro**: Credenciais em arquivo separado (não versionado)
- **Simples**: Um comando faz tudo
- **Versionado**: Controle automático de versões
- **Profissional**: Stack gerado dinamicamente

## 🎯 Resultado

Independente da configuração, você sempre terá:
- ✅ Imagem Docker versionada
- ✅ Stack personalizado gerado
- ✅ Comandos prontos para o servidor
- ✅ Deploy reproduzível 