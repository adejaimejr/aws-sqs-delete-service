# AWS SQS Delete Service

> **Serviço FastAPI para deletar mensagens do AWS SQS via endpoint HTTP - Perfeito para integração com n8n**

**[🇺🇸 English Version](README.md)**

## 🚀 Visão Geral

Este projeto foi criado para **simplificar drasticamente** o uso do n8n com AWS SQS, especificamente para a **remoção de mensagens da fila**. Em vez de configurar integrações complexas ou usar múltiplas ferramentas, você pode usar este serviço como um endpoint HTTP simples no seu workflow n8n.

## 🎯 Problema que Resolve

### Sem este serviço:
- Configuração complexa de credenciais AWS no n8n
- Múltiplas etapas para autenticação e remoção de mensagens
- Gerenciamento de tokens e sessões AWS
- Código repetitivo em workflows

### Com este serviço:
- **Um único endpoint HTTP** (`POST /delete-message`)
- **Configuração centralizada** de credenciais AWS
- **Resposta instantânea** (sucesso/erro)
- **Integração direta** com qualquer workflow n8n

## 🛠️ Como Funciona

Este serviço Python utiliza **recursos avançados** para executar a tarefa:

### Tecnologias Utilizadas:
- **FastAPI** - Framework web moderno e rápido
- **boto3** - SDK oficial da AWS para Python
- **asyncio** - Programação assíncrona para alta performance
- **Docker** - Containerização para deploy consistente
- **Uvicorn** - Servidor ASGI de alta performance

### Arquitetura:
```
n8n Workflow → HTTP POST → AWS SQS Delete Service → AWS SQS → Resposta
```

## 🔧 Configuração Rápida

### 1. Configure as variáveis de ambiente:
```bash
cp config.env.example .env
# Edite .env com suas credenciais AWS
```

### 2. Execute com Docker:
```bash
# Build e Deploy
./deploy.sh

# Ou manualmente
docker build -t aws-sqs-remove .
docker run -p 8000:8000 --env-file .env aws-sqs-remove
```

### 3. Use no n8n:
```json
{
  "method": "POST",
  "url": "http://seu-servidor:8000/delete-message",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/sua-fila",
    "receipt_handle": "AQEBwJ..."
  }
}
```

## 📡 API Endpoints

### `POST /delete-message`
Remove uma mensagem específica da fila SQS.

**Body:**
```json
{
  "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/sua-fila",
  "receipt_handle": "AQEBwJ..."
}
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "message": "Mensagem removida com sucesso"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Descrição do erro"
}
```

### `GET /health`
Verifica se o serviço está funcionando.

### `GET /docs`
Documentação interativa da API (Swagger UI).

## 🔒 Segurança

- **Credenciais AWS** gerenciadas via variáveis de ambiente
- **Validação de entrada** para todos os parâmetros
- **Logs detalhados** para auditoria
- **Suporte a HTTPS** quando configurado com proxy reverso

## 📁 Estrutura do Projeto

```
├── main.py              # Código principal da API
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── deploy.sh           # Script de deploy automatizado
├── config.env.example  # Template de configuração
├── SETUP.md           # Guia de configuração detalhado (Inglês)
├── SETUP-PT.md        # Guia de configuração detalhado (Português)
├── DEPLOY.md          # Instruções de deploy (Inglês)
├── DEPLOY-PT.md       # Instruções de deploy (Português)
└── VERSION            # Controle de versão
```

## 🚀 Vantagens para n8n

### Antes (Complexo):
1. Configurar credenciais AWS no n8n
2. Criar múltiplos nós para autenticação
3. Gerenciar tokens e sessões
4. Tratar erros individualmente
5. Repetir configuração em cada workflow

### Agora (Simples):
1. Um único nó HTTP Request no n8n
2. Endpoint padronizado
3. Resposta consistente
4. Tratamento centralizado de erros
5. Reutilização em todos os workflows

## 🌟 Recursos Avançados

- **Async/Await**: Operações não-bloqueantes para alta performance
- **Retry Logic**: Tentativas automáticas em caso de falha temporária
- **Rate Limiting**: Controle de taxa de requisições
- **Health Checks**: Monitoramento de saúde da aplicação
- **Logging Estruturado**: Logs detalhados para debugging
- **Error Handling**: Tratamento robusto de erros AWS

## 🧪 Testando

Teste o serviço com curl:

```bash
# Verificação de saúde
curl http://localhost:8000/health

# Deletar mensagem
curl -X POST http://localhost:8000/delete-message \
  -H "Content-Type: application/json" \
  -d '{
    "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/sua-fila",
    "receipt_handle": "seu-receipt-handle"
  }'
```

## 📖 Documentação Adicional

- [SETUP.md](SETUP.md) - Configuração detalhada (Inglês)
- [SETUP-PT.md](SETUP-PT.md) - Configuração detalhada (Português)
- [DEPLOY.md](DEPLOY.md) - Instruções de deploy (Inglês)
- [DEPLOY-PT.md](DEPLOY-PT.md) - Instruções de deploy (Português)
- [VERSION](VERSION) - Controle de versão

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests
- Compartilhar casos de uso

---

**Desenvolvido com ❤️ para simplificar a integração entre n8n e AWS SQS** 