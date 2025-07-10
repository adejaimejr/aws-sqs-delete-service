# 🚀 Deploy Simplificado - AWS SQS Delete Service

**[🇺🇸 English Version](DEPLOY.md)**

## ⚡ Deploy em Um Comando

```bash
./deploy.sh
```

Este script único faz **TUDO**:
- ✅ Versionamento automático
- ✅ Build da imagem Docker
- ✅ Push para Docker Hub
- ✅ Gera stack-producao.yaml automaticamente (usando variáveis)
- ✅ Fornece comandos para o servidor
- ✅ **Totalmente configurável via .env**

## ⚙️ Configuração (Opcional)

### 1. Criar Arquivo de Configuração
```bash
# Copiar exemplo
cp config.env.example .env

# Editar configurações
nano .env
```

### 2. Principais Variáveis
```bash
# Deploy
SERVICE_NAME=aws-sqs-delete
DOMAIN=sqs-api.example.com
NETWORK_NAME=network_swarm_public
LOGS_VOLUME_PATH=/opt/docker/logs/aws-sqs
DOCKER_IMAGE=your-registry/aws-sqs-remove

# AWS
AWS_ACCESS_KEY_ID=sua_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_DEFAULT_REGION=us-east-2

# API
API_PASSWORD=sua_senha_api
```

## 🎯 Como Usar

### 1. Executar o Script
```bash
./deploy.sh
```

### 2. Escolher Tipo de Versão
```
1) Patch (1.0.1 → 1.0.2) - Correções de bugs
2) Minor (1.0.1 → 1.1.0) - Novas funcionalidades  
3) Major (1.0.1 → 2.0.0) - Mudanças breaking
4) Personalizada - Definir versão manualmente
```

### 3. Confirmar Build
O script mostra a nova versão e pede confirmação.

### 4. Aguardar Build
Build automático multi-arquitetura (AMD64 + ARM64).

### 5. Usar Comandos no Servidor
O script fornece os comandos prontos para executar no servidor.

## 📁 Arquivos Gerados

- **`VERSION`** - Atualizado automaticamente
- **`stack-producao.yaml`** - Gerado com a nova versão

## 🖥️ Comandos no Servidor

```bash
# Remover stack atual
docker stack rm aws-sqs-delete

# Aguardar limpeza
sleep 15

# Pull da nova imagem
docker pull your-registry/aws-sqs-remove:X.X.X

# Deploy do novo stack
docker stack deploy -c stack-producao.yaml aws-sqs-delete

# Verificar
docker service ls | grep aws-sqs-delete
curl -k https://your-domain.com/health
```

## ✨ Vantagens

- **Simplicidade**: Um único script para tudo
- **Automação**: Zero configuração manual
- **Versionamento**: Semântico e automático
- **Template**: Stack gerado dinamicamente com variáveis
- **Flexibilidade**: Totalmente configurável via .env
- **Reutilização**: Mesmo script para diferentes ambientes
- **Segurança**: Credenciais em arquivo separado

## 🎉 Resultado

Ao final, você terá:
- ✅ Imagem Docker versionada no Docker Hub
- ✅ Stack de produção atualizado (com suas configurações)
- ✅ Comandos prontos para o servidor
- ✅ Versionamento controlado
- ✅ **Projeto totalmente configurável e reutilizável**

## 🔄 Diferentes Ambientes

```bash
# Desenvolvimento
cp config.env.example .env.dev
# Editar .env.dev
cp .env.dev .env && ./deploy.sh

# Produção  
cp config.env.example .env.prod
# Editar .env.prod
cp .env.prod .env && ./deploy.sh
``` 