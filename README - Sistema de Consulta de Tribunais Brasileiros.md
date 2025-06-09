# README - Sistema de Consulta de Tribunais Brasileiros

🏛️ **Sistema de Consulta Unificada de Tribunais com Integração Claude MCP**

Uma solução completa e econômica para consultar processos judiciais em múltiplos tribunais brasileiros, com integração nativa ao Claude via Model Context Protocol (MCP).

## 🚀 Características Principais

- ✅ **28+ Tribunais Suportados** - STF, STJ, TST, TRFs, TJs, TRTs
- ✅ **Integração Claude MCP** - Consultas em linguagem natural
- ✅ **Interface Web Moderna** - Design responsivo e intuitivo
- ✅ **API REST Completa** - Endpoints para todas as funcionalidades
- ✅ **Validação Automática** - Formatação e verificação de números de processo
- ✅ **Consultas Múltiplas** - Busca simultânea em vários tribunais
- ✅ **Monitoramento Real-time** - Status e conectividade dos tribunais
- ✅ **Deploy Simples** - Pronto para Railway, Heroku, DigitalOcean

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Claude MCP    │◄──►│   Backend API    │◄──►│  Interface Web  │
│   (5 tools)     │    │   (Flask)        │    │   (HTML/JS)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  APIs Tribunais  │
                       │   (Datajud CNJ)  │
                       └──────────────────┘
```

## 📦 Instalação Rápida

### 1. Backend API

```bash
# Clonar projeto
git clone <repository-url>
cd tribunal-api

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python src/main.py
```

### 2. Servidor MCP

```bash
# Instalar dependências MCP
pip install mcp httpx

# Testar servidor
python3 tribunal-mcp-server.py
```

### 3. Configurar Claude Desktop

Adicione ao `claude_desktop_config.json`:

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

**Localização do arquivo:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

## 🛠️ Uso

### Interface Web
Acesse `http://localhost:5001` para usar a interface visual.

### Claude Desktop
Após configurar o MCP, use comandos naturais:

```
"Consulte o processo número 1234567-89.0123.4.56.7890"
"Liste todos os tribunais disponíveis"
"Valide o número 12345678901234567890"
"Consulte o processo X em múltiplos tribunais"
"Qual o status do sistema?"
```

### API REST

```bash
# Listar tribunais
curl http://localhost:5001/api/tribunais

# Validar processo
curl http://localhost:5001/api/validar/12345678901234567890

# Consultar processo
curl http://localhost:5001/api/processo/1234567890123456789

# Status do sistema
curl http://localhost:5001/api/status
```

## 🚀 Guia de Deploy Detalhado

Para um passo a passo completo sobre como fazer o deploy do seu projeto no Railway, Heroku, Docker ou VPS, incluindo a configuração do Git e a integração com o Claude via MCP, consulte o [Guia de Deploy Detalhado](deploy_guide.md).

**Sobre Autenticação (Login e Senha):**

É importante notar que este projeto, em sua versão atual, utiliza a API Pública do Datajud do CNJ, que **não requer autenticação (login e senha)** para consultas de processos públicos. Isso simplifica o uso e reduz custos. Para cenários futuros que exijam integração com APIs de tribunais que demandam login e senha (como PJE, eproc, eSAJ), o [Guia de Deploy Detalhado](deploy_guide.md) também explica como a arquitetura pode ser expandida para gerenciar essas credenciais de forma segura.

## 📊 Tribunais Suportados

| Tipo | Tribunais | Quantidade |
|------|-----------|------------|
| **Superiores** | STF, STJ, TST, TSE, STM | 5 |
| **Federais** | TRF1, TRF2, TRF3, TRF4, TRF5, TRF6 | 6 |
| **Estaduais** | TJSP, TJRJ, TJMG, TJRS, TJPR, TJSC, etc. | 11 |
| **Trabalho** | TRT1, TRT2, TRT3, TRT4, TRT5, TRT15 | 6 |
| **Total** | | **28+** |

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# API Configuration
API_BASE_URL=http://localhost:5001/api
FLASK_ENV=production
FLASK_DEBUG=false

# Cache Configuration
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### Customização

```python
# Adicionar novo tribunal
TRIBUNAIS_CUSTOM = {
    'tjxx': 'Tribunal de Justiça do Estado XX'
}

# Configurar timeout
REQUEST_TIMEOUT = 30

# Configurar retry
MAX_RETRIES = 3
```

## 📈 Monitoramento

### Métricas Disponíveis
- Status da API (online/offline)
- Conectividade por tribunal
- Tempo de resposta médio
- Taxa de sucesso/erro
- Número de consultas por período

### Logs
```bash
# Ver logs em tempo real
tail -f logs/tribunal-api.log

# Filtrar erros
grep "ERROR" logs/tribunal-api.log
```

## 💰 Custos Estimados

| Ambiente | Custo Mensal | Recursos |
|----------|--------------|----------|
| **Desenvolvimento** | $0 | Local |
| **Pessoal/Pequeno** | $15-35 | Railway/Heroku básico |
| **Empresarial** | $100-500 | Multi-instância, cache, monitoramento |
| **Enterprise** | $500+ | Alta disponibilidade, SLA |

## 🔒 Segurança

- ✅ HTTPS obrigatório em produção
- ✅ Rate limiting por IP
- ✅ Validação rigorosa de entrada
- ✅ Logs de auditoria
- ✅ Não armazenamento de dados sensíveis
- ✅ Compliance LGPD

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de conexão com tribunais:**
```bash
# Verificar conectividade
curl http://localhost:5001/api/status
```

**MCP não funciona no Claude:**
```bash
# Verificar configuração
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Servidor não inicia:**
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar porta
lsof -i :5001
```

## 📚 Documentação

- 📖 [Documentação Completa](documentacao_completa.md)
- 🔧 [Guia de API](api_documentation.md)
- 🚀 [Guia de Deploy](deploy_guide.md)
- 🤖 [Integração MCP](MCP_README.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 🐛 **Issues:** [GitHub Issues](https://github.com/seu-usuario/tribunal-api/issues)
- 💬 **Discord:** [Comunidade](https://discord.gg/tribunal-api)
- 📧 **Email:** suporte@tribunal-api.com
- 📞 **Consultoria:** contato@tribunal-api.com

## 🎯 Roadmap

### v1.1 (Próxima)
- [ ] Cache Redis distribuído
- [ ] Interface mobile
- [ ] Relatórios em PDF
- [ ] Notificações por email

### v1.2 (Futuro)
- [ ] API pública
- [ ] Integração PJE específica
- [ ] Analytics avançado
- [ ] Webhooks

### v2.0 (Visão)
- [ ] IA para análise de processos
- [ ] Predição de resultados
- [ ] Assistente virtual
- [ ] Automação workflows

---

**Desenvolvido com ❤️ por [Manus AI](https://manus.ai)**

*Transformando o acesso à informação jurídica através de tecnologia acessível e eficiente.*

