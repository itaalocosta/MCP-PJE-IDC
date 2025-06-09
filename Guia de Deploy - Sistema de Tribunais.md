# Guia de Deploy - Sistema de Tribunais

## 🚀 Opções de Deploy

### 1. Railway (Recomendado)

**Vantagens:**
- Deploy automático via Git
- SSL gratuito
- Domínio personalizado
- Fácil configuração
- Custo baixo ($5-20/mês)

**Passos:**

1. **Criar conta no Railway**
   - Acesse [railway.app](https://railway.app)
   - Conecte com GitHub

2. **Preparar repositório**
   ```bash
   # Criar repositório Git
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <seu-repo-url>
   git push -u origin main
   ```

3. **Configurar Railway**
   - New Project → Deploy from GitHub
   - Selecionar repositório
   - Railway detecta automaticamente Python

4. **Configurar variáveis de ambiente**
   ```
   PORT=5001
   FLASK_ENV=production
   PYTHONPATH=/app
   ```

5. **Deploy automático**
   - Cada push no main faz deploy automático
   - URL gerada automaticamente

### 2. Heroku

**Preparação:**

1. **Criar Procfile**
   ```
   web: python src/main.py
   ```

2. **Configurar runtime.txt**
   ```
   python-3.11.0
   ```

3. **Deploy**
   ```bash
   # Instalar Heroku CLI
   heroku login
   heroku create tribunal-api-seu-nome
   
   # Configurar variáveis
   heroku config:set FLASK_ENV=production
   heroku config:set PORT=5001
   
   # Deploy
   git push heroku main
   ```

### 3. DigitalOcean App Platform

1. **Conectar repositório**
   - Apps → Create App
   - Conectar GitHub

2. **Configurar build**
   ```yaml
   name: tribunal-api
   services:
   - name: web
     source_dir: /
     github:
       repo: seu-usuario/tribunal-api
       branch: main
     run_command: python src/main.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
   ```

### 4. VPS Manual

**Para Ubuntu 20.04+:**

1. **Configurar servidor**
   ```bash
   # Atualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar Python e dependências
   sudo apt install python3 python3-pip python3-venv nginx -y
   
   # Criar usuário
   sudo adduser tribunal
   sudo usermod -aG sudo tribunal
   ```

2. **Deploy aplicação**
   ```bash
   # Clonar projeto
   git clone <repo-url> /home/tribunal/app
   cd /home/tribunal/app
   
   # Criar ambiente virtual
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar systemd**
   ```ini
   # /etc/systemd/system/tribunal-api.service
   [Unit]
   Description=Tribunal API
   After=network.target
   
   [Service]
   User=tribunal
   WorkingDirectory=/home/tribunal/app
   Environment=PATH=/home/tribunal/app/venv/bin
   ExecStart=/home/tribunal/app/venv/bin/python src/main.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Configurar Nginx**
   ```nginx
   # /etc/nginx/sites-available/tribunal-api
   server {
       listen 80;
       server_name seu-dominio.com;
       
       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Ativar serviços**
   ```bash
   sudo systemctl enable tribunal-api
   sudo systemctl start tribunal-api
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash tribunal
RUN chown -R tribunal:tribunal /app
USER tribunal

# Expor porta
EXPOSE 5001

# Comando de inicialização
CMD ["python", "src/main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tribunal-api:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - tribunal-api
    restart: unless-stopped
```

### Build e Deploy

```bash
# Build local
docker build -t tribunal-api .

# Run local
docker run -p 5001:5001 tribunal-api

# Docker Compose
docker-compose up -d

# Deploy para registry
docker tag tribunal-api registry.digitalocean.com/seu-registry/tribunal-api
docker push registry.digitalocean.com/seu-registry/tribunal-api
```

## ☁️ Kubernetes

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tribunal-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tribunal-api
  template:
    metadata:
      labels:
        app: tribunal-api
    spec:
      containers:
      - name: tribunal-api
        image: tribunal-api:latest
        ports:
        - containerPort: 5001
        env:
        - name: FLASK_ENV
          value: "production"
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: tribunal-api-service
spec:
  selector:
    app: tribunal-api
  ports:
  - port: 80
    targetPort: 5001
  type: LoadBalancer
```

## 🔧 Configurações de Produção

### Variáveis de Ambiente

```bash
# Aplicação
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=sua-chave-secreta-super-forte

# Database/Cache
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@host:5432/db

# APIs
DATAJUD_API_KEY=sua-chave-api
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# Segurança
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
ALLOWED_ORIGINS=https://seu-dominio.com

# Monitoramento
SENTRY_DSN=https://sua-chave@sentry.io/projeto
LOG_LEVEL=INFO
```

### Nginx Configuração

```nginx
server {
    listen 80;
    server_name tribunal-api.com www.tribunal-api.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tribunal-api.com www.tribunal-api.com;

    ssl_certificate /etc/letsencrypt/live/tribunal-api.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tribunal-api.com/privkey.pem;

    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Headers de segurança
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location / {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache para assets estáticos
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📊 Monitoramento

### Health Check

```python
# Adicionar ao Flask app
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_duration_seconds', 'Request latency')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if app.config['FLASK_ENV'] == 'production':
    file_handler = RotatingFileHandler(
        'logs/tribunal-api.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 🔒 Segurança

### SSL/TLS

```bash
# Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tribunal-api.com
sudo certbot renew --dry-run
```

### Firewall

```bash
# UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup código
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/tribunal/app

# Backup configurações
cp /etc/nginx/sites-available/tribunal-api $BACKUP_DIR/nginx_$DATE.conf
cp /etc/systemd/system/tribunal-api.service $BACKUP_DIR/systemd_$DATE.service

# Limpar backups antigos (manter 7 dias)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 📈 Escalabilidade

### Load Balancer

```nginx
upstream tribunal_api {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    location / {
        proxy_pass http://tribunal_api;
    }
}
```

### Auto Scaling (AWS)

```yaml
# auto-scaling-group.yaml
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 3
      TargetGroupARNs:
        - !Ref TargetGroup
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
```

## 🚨 Troubleshooting

### Problemas Comuns

**1. Aplicação não inicia**
```bash
# Verificar logs
journalctl -u tribunal-api -f

# Verificar porta
sudo netstat -tlnp | grep :5001

# Verificar permissões
ls -la /home/tribunal/app
```

**2. Erro 502 Bad Gateway**
```bash
# Verificar se app está rodando
curl http://127.0.0.1:5001/health

# Verificar configuração Nginx
sudo nginx -t

# Verificar logs Nginx
sudo tail -f /var/log/nginx/error.log
```

**3. Performance lenta**
```bash
# Verificar recursos
htop
df -h
free -m

# Verificar conexões
ss -tuln
```

### Comandos Úteis

```bash
# Restart serviços
sudo systemctl restart tribunal-api
sudo systemctl restart nginx

# Ver logs em tempo real
tail -f logs/tribunal-api.log
journalctl -u tribunal-api -f

# Verificar status
systemctl status tribunal-api
systemctl status nginx

# Teste de carga
ab -n 1000 -c 10 http://localhost:5001/api/status
```

---

**Deploy realizado com sucesso! 🎉**

Para suporte adicional, consulte a [documentação completa](documentacao_completa.md) ou entre em contato através dos canais de suporte.




## 🚀 Guia de Deploy Detalhado no Railway (Passo a Passo)

Este guia detalha o processo de deploy do seu sistema de consulta de tribunais no Railway, uma plataforma de hospedagem que oferece simplicidade e eficiência para aplicações web. Ao final, você terá um link público para sua API e interface web, pronto para ser integrado ao Claude via MCP.

### Pré-requisitos:

*   Uma conta no [GitHub](https://github.com/)
*   Uma conta no [Railway](https://railway.app/)
*   Git instalado na sua máquina local
*   O código-fonte do projeto (`tribunal-api` e `tribunal-mcp-server.py`) em seu ambiente local.

### Passo 1: Preparar o Projeto para o Git

Se você ainda não inicializou um repositório Git para o seu projeto, siga estes passos. É crucial que o diretório `tribunal-api` e o arquivo `tribunal-mcp-server.py` estejam no mesmo repositório ou que você os organize de forma que o Railway possa acessá-los.

1.  **Navegue até o diretório raiz do seu projeto** (onde `tribunal-api` e `tribunal-mcp-server.py` estão localizados):

    ```bash
    cd /home/ubuntu/  # Ou o diretório onde você salvou os arquivos
    ```

2.  **Inicialize um repositório Git (se ainda não o fez):**

    ```bash
    git init
    ```

3.  **Adicione todos os arquivos do projeto ao repositório:**

    ```bash
    git add .
    ```

4.  **Faça o primeiro commit:**

    ```bash
    git commit -m "Initial commit: Tribunal API and MCP Server"
    ```

5.  **Crie um repositório vazio no GitHub** (ex: `tribunal-api-mcp`). Não adicione README, .gitignore ou licença neste momento, pois você já tem os arquivos localmente.

6.  **Conecte seu repositório local ao GitHub:**

    ```bash
    git remote add origin https://github.com/SEU_USUARIO/tribunal-api-mcp.git  # Substitua SEU_USUARIO e tribunal-api-mcp
    git branch -M main
    git push -u origin main
    ```

    Seus arquivos agora estão no GitHub, prontos para o deploy.

### Passo 2: Deploy no Railway

O Railway facilita o deploy de aplicações Python. Siga estes passos para colocar seu sistema online:

1.  **Acesse o Railway e crie um novo projeto:**

    *   Vá para [railway.app](https://railway.app/) e faça login.
    *   Clique em `New Project`.
    *   Selecione `Deploy from GitHub Repo`.

2.  **Conecte seu repositório:**

    *   Selecione o repositório que você acabou de criar (`tribunal-api-mcp`).
    *   O Railway irá detectar automaticamente que é um projeto Python.

3.  **Configurar o Serviço (Backend API):**

    *   Após a detecção, o Railway criará um serviço. Clique nele para configurar.
    *   Vá para a aba `Settings`.
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `python src/main.py`
    *   **Root Directory:** Certifique-se de que está apontando para o diretório raiz do seu projeto (onde `src` e `tribunal-mcp-server.py` estão). Se você organizou o projeto com `tribunal-api` como subdiretório, o `Root Directory` deve ser `tribunal-api`.
    *   **Port:** O Railway geralmente expõe a porta 80/443. Certifique-se de que seu Flask app está configurado para escutar em `0.0.0.0` e na porta `5001` (ou a porta que o Railway atribuir via variável de ambiente `PORT`). No seu `src/main.py`, a linha `app.run(host='0.0.0.0', port=5001, debug=True)` já atende a isso.

4.  **Configurar Variáveis de Ambiente:**

    *   Vá para a aba `Variables`.
    *   Adicione as seguintes variáveis:
        *   `FLASK_ENV`: `production`
        *   `PYTHONPATH`: `/app` (ou `/app/tribunal-api` se seu projeto estiver em um subdiretório)
        *   `PORT`: `5001` (ou a porta que o Railway sugerir)

5.  **Aguarde o Deploy:**

    *   O Railway iniciará o processo de build e deploy. Você pode acompanhar o progresso na aba `Deployments`.
    *   Uma vez que o deploy esteja completo, o Railway fornecerá uma URL pública para o seu serviço (ex: `https://tribunal-api-xxxx.up.railway.app/`).

### Passo 3: Usar o Link de Integração no Claude

Com seu backend e interface web rodando no Railway, você pode usar o link público para integrar com o Claude via MCP.

1.  **Obtenha a URL Pública do seu Serviço Railway:**

    *   Na dashboard do Railway, vá para o seu serviço e copie a URL fornecida. Será algo como `https://tribunal-api-xxxx.up.railway.app/`.

2.  **Atualize o `API_BASE_URL` no seu `tribunal-mcp-server.py`:**

    *   No arquivo `tribunal-mcp-server.py` (que você executará localmente para o Claude Desktop), altere a linha:

        ```python
        API_BASE_URL = "http://localhost:5001/api"
        ```

        Para:

        ```python
        API_BASE_URL = "https://tribunal-api-xxxx.up.railway.app/api"  # Substitua pela sua URL do Railway
        ```

    *   Salve o arquivo `tribunal-mcp-server.py` atualizado.

3.  **Execute o Servidor MCP Localmente:**

    *   Abra um terminal no seu computador local e execute:

        ```bash
        python3 /home/ubuntu/tribunal-mcp-server.py  # Ou o caminho correto para o arquivo
        ```

    *   Este servidor MCP local atuará como uma ponte entre o Claude Desktop e sua API hospedada no Railway.

4.  **Configure o Claude Desktop:**

    *   Conforme detalhado no `MCP_README.md`, adicione a configuração do `mcpServers` ao seu `claude_desktop_config.json`.
    *   Certifique-se de que o `command` e `args` apontam para o `python3` e o caminho correto do seu `tribunal-mcp-server.py` local.

    ```json
    {
      "mcpServers": {
        "tribunal-mcp": {
          "command": "python3",
          "args": ["/caminho/para/tribunal-mcp-server.py"]
        }
      }
    }
    ```

5.  **Reinicie o Claude Desktop:**

    *   Após salvar as configurações, reinicie o Claude Desktop para que ele reconheça o novo servidor MCP e suas ferramentas.

Agora, quando você usar as ferramentas no Claude (ex: `consultar_processo`), o Claude enviará a requisição para o seu servidor MCP local, que por sua vez, fará a chamada para a sua API hospedada no Railway, que então consultará o Datajud e retornará o resultado ao Claude.

## 🔒 Autenticação de APIs de Tribunais (Login e Senha)

Atualmente, este projeto utiliza a **API Pública do Datajud do CNJ**, que **não requer autenticação (login e senha)** para realizar consultas de processos públicos. Isso torna a solução mais simples e barata de operar, pois não há necessidade de gerenciar credenciais complexas para cada tribunal.

### Cenários Futuros com Autenticação:

Caso haja a necessidade de integrar com APIs de tribunais que exigem login e senha (como algumas APIs específicas do PJE, eproc ou eSAJ que oferecem dados mais detalhados ou funcionalidades restritas), a arquitetura pode ser expandida da seguinte forma:

1.  **Gerenciamento de Credenciais no Backend:**
    *   O backend (Flask API) seria o local ideal para armazenar e gerenciar as credenciais de acesso a esses tribunais. Isso pode ser feito de forma segura através de:
        *   **Variáveis de Ambiente:** Para credenciais sensíveis que não mudam com frequência (ex: chaves de API).
        *   **Banco de Dados Criptografado:** Para credenciais de usuários que precisam ser gerenciadas dinamicamente (ex: um usuário insere seu login e senha do PJE).
        *   **Serviços de Gerenciamento de Segredos:** Plataformas de nuvem como AWS Secrets Manager ou Google Secret Manager oferecem soluções robustas para armazenar e acessar segredos de forma segura.

2.  **Endpoints de Autenticação:**
    *   Seriam criados endpoints específicos na API do backend para que o usuário possa fornecer suas credenciais. Por exemplo:
        *   `POST /api/credenciais/pje` - Para enviar login e senha do PJE.
        *   `POST /api/credenciais/eproc` - Para enviar login e senha do eproc.

3.  **Fluxo de Autenticação:**
    *   Quando uma consulta for feita a um tribunal que exige autenticação, o backend usaria as credenciais armazenadas para se autenticar na API do tribunal antes de realizar a consulta.
    *   Isso garante que as credenciais nunca sejam expostas diretamente na interface web ou no servidor MCP.

4.  **Interface Web para Credenciais:**
    *   A interface web atual poderia ser expandida com uma nova aba ou seção para que o usuário possa inserir e gerenciar suas credenciais de acesso a tribunais específicos.

**Importante:** A implementação de autenticação para APIs de tribunais que exigem login e senha é um recurso mais avançado e não faz parte do escopo inicial deste projeto para manter a simplicidade e o baixo custo. No entanto, a arquitetura foi projetada para permitir essa expansão no futuro, caso seja necessário acessar funcionalidades ou dados que não estão disponíveis via API Pública do Datajud.

