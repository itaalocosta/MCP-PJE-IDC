# Servidor MCP para Tribunais Brasileiros

Este é um servidor MCP (Model Context Protocol) que permite ao Claude consultar processos judiciais em tribunais brasileiros.

## Instalação

1. Instale as dependências:
```bash
pip install mcp httpx
```

2. Certifique-se de que a API de tribunais está rodando na porta 5001:
```bash
cd tribunal-api
source venv/bin/activate
python src/main.py
```

3. Configure o Claude Desktop adicionando ao arquivo de configuração:

**No macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**No Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "tribunal-mcp": {
      "command": "python3",
      "args": ["/caminho/para/tribunal-mcp-server.py"],
      "env": {
        "PYTHONPATH": "/caminho/para/diretorio"
      }
    }
  }
}
```

## Ferramentas Disponíveis

### 1. consultar_processo
Consulta informações de um processo judicial brasileiro.

**Parâmetros:**
- `numero_processo` (obrigatório): Número do processo judicial (20 dígitos)
- `tribunal` (opcional): Código do tribunal específico (ex: tjsp, stj, trf1)

### 2. listar_tribunais
Lista todos os tribunais disponíveis para consulta.

### 3. validar_processo
Valida o formato de um número de processo judicial.

**Parâmetros:**
- `numero_processo` (obrigatório): Número do processo para validar

### 4. consulta_multipla
Consulta um processo em múltiplos tribunais simultaneamente.

**Parâmetros:**
- `numero_processo` (obrigatório): Número do processo judicial
- `tribunais` (opcional): Lista de códigos de tribunais para consultar

### 5. status_sistema
Verifica o status do sistema e conectividade com tribunais.

## Exemplo de Uso no Claude

Após configurar o MCP, você pode fazer perguntas como:

- "Consulte o processo número 12345678901234567890"
- "Liste todos os tribunais disponíveis"
- "Valide o número de processo 1234567890123456789"
- "Consulte o processo 12345678901234567890 nos tribunais TJSP e STJ"
- "Qual o status do sistema de tribunais?"

## Tribunais Suportados

O sistema suporta 28+ tribunais brasileiros, incluindo:

- **Tribunais Superiores:** STF, STJ, TSE, TST, STM
- **Justiça Federal:** TRF1, TRF2, TRF3, TRF4, TRF5, TRF6
- **Justiça Estadual:** TJSP, TJRJ, TJMG, TJRS, TJPR, TJSC, etc.
- **Justiça do Trabalho:** TRT1, TRT2, TRT3, TRT4, TRT5, TRT15, etc.

## Troubleshooting

1. **Erro de conexão:** Verifique se a API de tribunais está rodando na porta 5001
2. **Servidor MCP não inicia:** Verifique se as dependências estão instaladas
3. **Claude não reconhece as ferramentas:** Verifique a configuração do claude_desktop_config.json

## Logs

O servidor MCP gera logs para debug. Para ver os logs:
```bash
python3 tribunal-mcp-server.py
```

