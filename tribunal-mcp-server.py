#!/usr/bin/env python3
"""
Servidor MCP para Integração com Tribunais Brasileiros
Permite que o Claude consulte processos judiciais através do Model Context Protocol
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
import mcp.server.stdio
import mcp.types as types

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tribunal-mcp")

# URL base da API de tribunais
API_BASE_URL = "http://localhost:5001/api"

class TribunalMCPServer:
    def __init__(self):
        self.server = Server("tribunal-mcp")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configura os handlers do servidor MCP"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Lista todas as ferramentas disponíveis"""
            return [
                types.Tool(
                    name="consultar_processo",
                    description="Consulta informações de um processo judicial brasileiro",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "numero_processo": {
                                "type": "string",
                                "description": "Número do processo judicial (20 dígitos)"
                            },
                            "tribunal": {
                                "type": "string",
                                "description": "Código do tribunal específico (opcional). Ex: tjsp, stj, trf1"
                            }
                        },
                        "required": ["numero_processo"]
                    }
                ),
                types.Tool(
                    name="listar_tribunais",
                    description="Lista todos os tribunais disponíveis para consulta",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="validar_processo",
                    description="Valida o formato de um número de processo judicial",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "numero_processo": {
                                "type": "string",
                                "description": "Número do processo para validar"
                            }
                        },
                        "required": ["numero_processo"]
                    }
                ),
                types.Tool(
                    name="consulta_multipla",
                    description="Consulta um processo em múltiplos tribunais simultaneamente",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "numero_processo": {
                                "type": "string",
                                "description": "Número do processo judicial"
                            },
                            "tribunais": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Lista de códigos de tribunais para consultar (opcional)"
                            }
                        },
                        "required": ["numero_processo"]
                    }
                ),
                types.Tool(
                    name="status_sistema",
                    description="Verifica o status do sistema e conectividade com tribunais",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Executa uma ferramenta específica"""
            
            try:
                if name == "consultar_processo":
                    return await self._consultar_processo(arguments)
                elif name == "listar_tribunais":
                    return await self._listar_tribunais()
                elif name == "validar_processo":
                    return await self._validar_processo(arguments)
                elif name == "consulta_multipla":
                    return await self._consulta_multipla(arguments)
                elif name == "status_sistema":
                    return await self._status_sistema()
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"Ferramenta desconhecida: {name}"
                    )]
            except Exception as e:
                logger.error(f"Erro ao executar ferramenta {name}: {str(e)}")
                return [types.TextContent(
                    type="text",
                    text=f"Erro ao executar {name}: {str(e)}"
                )]

    async def _fazer_requisicao(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP para a API de tribunais"""
        url = f"{API_BASE_URL}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            if params:
                response = await client.post(url, json=params)
            else:
                response = await client.get(url)
            
            response.raise_for_status()
            return response.json()

    async def _consultar_processo(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Consulta um processo judicial"""
        numero_processo = arguments.get("numero_processo")
        tribunal = arguments.get("tribunal")
        
        if not numero_processo:
            return [types.TextContent(
                type="text",
                text="Erro: Número do processo é obrigatório"
            )]
        
        try:
            if tribunal:
                # Consulta em tribunal específico
                endpoint = f"/tribunal/{tribunal}/processo/{numero_processo}"
            else:
                # Consulta com detecção automática de tribunal
                endpoint = f"/processo/{numero_processo}"
            
            resultado = await self._fazer_requisicao(endpoint)
            
            if resultado.get("sucesso"):
                dados = resultado.get("dados", {})
                tribunal_nome = resultado.get("tribunal", "Desconhecido")
                
                resposta = f"""
**Processo Encontrado!**

📋 **Número:** {numero_processo}
🏛️ **Tribunal:** {tribunal_nome}
📊 **Fonte:** {resultado.get("fonte", "API")}

**Informações do Processo:**
"""
                
                # Adiciona informações específicas se disponíveis
                if isinstance(dados, dict):
                    for chave, valor in dados.items():
                        if valor:
                            resposta += f"• **{chave.replace('_', ' ').title()}:** {valor}\n"
                else:
                    resposta += f"• **Dados:** {dados}\n"
                
                return [types.TextContent(type="text", text=resposta)]
            else:
                erro = resultado.get("erro", "Erro desconhecido")
                return [types.TextContent(
                    type="text",
                    text=f"❌ **Processo não encontrado**\n\n**Número:** {numero_processo}\n**Erro:** {erro}"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ **Erro na consulta**\n\n**Número:** {numero_processo}\n**Erro:** {str(e)}"
            )]

    async def _listar_tribunais(self) -> List[types.TextContent]:
        """Lista todos os tribunais disponíveis"""
        try:
            resultado = await self._fazer_requisicao("/tribunais")
            
            if resultado.get("sucesso"):
                tribunais = resultado.get("tribunais", [])
                total = resultado.get("total", 0)
                
                resposta = f"🏛️ **Tribunais Disponíveis ({total} tribunais)**\n\n"
                
                # Agrupa por tipo de justiça
                tipos = {
                    "Tribunais Superiores": [],
                    "Justiça Federal": [],
                    "Justiça Estadual": [],
                    "Justiça do Trabalho": [],
                    "Outros": []
                }
                
                for tribunal in tribunais:
                    codigo = tribunal["codigo"]
                    nome = tribunal["nome"]
                    
                    if codigo in ["stf", "stj", "tse", "stm", "tst"]:
                        tipos["Tribunais Superiores"].append(f"• **{codigo.upper()}** - {nome}")
                    elif codigo.startswith("trf"):
                        tipos["Justiça Federal"].append(f"• **{codigo.upper()}** - {nome}")
                    elif codigo.startswith("tj"):
                        tipos["Justiça Estadual"].append(f"• **{codigo.upper()}** - {nome}")
                    elif codigo.startswith("trt"):
                        tipos["Justiça do Trabalho"].append(f"• **{codigo.upper()}** - {nome}")
                    else:
                        tipos["Outros"].append(f"• **{codigo.upper()}** - {nome}")
                
                for tipo, lista in tipos.items():
                    if lista:
                        resposta += f"\n**{tipo}:**\n"
                        resposta += "\n".join(lista) + "\n"
                
                resposta += f"\n💡 **Como usar:** Para consultar um processo específico, use o código do tribunal (ex: tjsp, stj, trf1)"
                
                return [types.TextContent(type="text", text=resposta)]
            else:
                return [types.TextContent(
                    type="text",
                    text="❌ Erro ao listar tribunais"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ Erro ao listar tribunais: {str(e)}"
            )]

    async def _validar_processo(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Valida formato de número de processo"""
        numero_processo = arguments.get("numero_processo")
        
        if not numero_processo:
            return [types.TextContent(
                type="text",
                text="Erro: Número do processo é obrigatório"
            )]
        
        try:
            resultado = await self._fazer_requisicao(f"/validar/{numero_processo}")
            
            if resultado.get("valido"):
                numero_formatado = resultado.get("numero_formatado")
                tribunal_identificado = resultado.get("tribunal_identificado")
                tribunal_nome = resultado.get("tribunal_nome")
                
                resposta = f"""
✅ **Número de Processo Válido**

📋 **Número Original:** {numero_processo}
📋 **Número Formatado:** {numero_formatado}
🏛️ **Tribunal Identificado:** {tribunal_identificado.upper()} - {tribunal_nome}

💡 **Próximo passo:** Use a ferramenta `consultar_processo` para obter informações detalhadas.
"""
                return [types.TextContent(type="text", text=resposta)]
            else:
                erro = resultado.get("erro", "Formato inválido")
                return [types.TextContent(
                    type="text",
                    text=f"❌ **Número de Processo Inválido**\n\n**Número:** {numero_processo}\n**Erro:** {erro}\n\n💡 **Formato correto:** O número deve conter exatamente 20 dígitos"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ Erro na validação: {str(e)}"
            )]

    async def _consulta_multipla(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Consulta processo em múltiplos tribunais"""
        numero_processo = arguments.get("numero_processo")
        tribunais = arguments.get("tribunais", [])
        
        if not numero_processo:
            return [types.TextContent(
                type="text",
                text="Erro: Número do processo é obrigatório"
            )]
        
        try:
            params = {"numero_processo": numero_processo}
            if tribunais:
                params["tribunais"] = tribunais
            
            resultado = await self._fazer_requisicao("/consulta/multipla", params)
            
            if resultado.get("sucesso"):
                numero_formatado = resultado.get("numero_processo")
                tribunais_consultados = resultado.get("tribunais_consultados", 0)
                encontrados = resultado.get("encontrados", 0)
                resultados = resultado.get("resultados", [])
                
                resposta = f"""
🔍 **Consulta Múltipla Realizada**

📋 **Processo:** {numero_formatado}
📊 **Tribunais Consultados:** {tribunais_consultados}
✅ **Encontrados:** {encontrados}

**Resultados:**
"""
                
                for resultado_tribunal in resultados:
                    tribunal_codigo = resultado_tribunal.get("tribunal_codigo", "").upper()
                    tribunal_nome = resultado_tribunal.get("tribunal", "Desconhecido")
                    sucesso = resultado_tribunal.get("sucesso", False)
                    
                    if sucesso:
                        resposta += f"\n✅ **{tribunal_codigo}** - {tribunal_nome}\n"
                        dados = resultado_tribunal.get("dados", {})
                        if isinstance(dados, dict) and dados:
                            for chave, valor in list(dados.items())[:3]:  # Mostra apenas os 3 primeiros campos
                                if valor:
                                    resposta += f"   • {chave.replace('_', ' ').title()}: {valor}\n"
                    else:
                        erro = resultado_tribunal.get("erro", "Não encontrado")
                        resposta += f"\n❌ **{tribunal_codigo}** - {tribunal_nome}: {erro}\n"
                
                if encontrados > 0:
                    resposta += f"\n💡 **Dica:** Use `consultar_processo` com tribunal específico para mais detalhes."
                
                return [types.TextContent(type="text", text=resposta)]
            else:
                erro = resultado.get("erro", "Erro na consulta múltipla")
                return [types.TextContent(
                    type="text",
                    text=f"❌ Erro na consulta múltipla: {erro}"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ Erro na consulta múltipla: {str(e)}"
            )]

    async def _status_sistema(self) -> List[types.TextContent]:
        """Verifica status do sistema"""
        try:
            resultado = await self._fazer_requisicao("/status")
            
            api_status = resultado.get("api_status", "unknown")
            timestamp = resultado.get("timestamp", "")
            total_tribunais = resultado.get("total_tribunais_disponiveis", 0)
            tribunais_testados = resultado.get("tribunais_testados", [])
            
            resposta = f"""
🔧 **Status do Sistema de Tribunais**

📊 **API Status:** {api_status.upper()}
🕐 **Última Verificação:** {timestamp}
🏛️ **Tribunais Disponíveis:** {total_tribunais}

**Conectividade dos Tribunais Testados:**
"""
            
            for tribunal in tribunais_testados:
                codigo = tribunal.get("tribunal", "").upper()
                nome = tribunal.get("nome", "")
                status = tribunal.get("status", "unknown")
                codigo_resposta = tribunal.get("codigo_resposta")
                
                emoji = "✅" if status == "online" else "❌"
                resposta += f"\n{emoji} **{codigo}** - {nome}"
                if codigo_resposta:
                    resposta += f" (HTTP {codigo_resposta})"
            
            resposta += f"\n\n💡 **Sistema operacional e pronto para consultas!**"
            
            return [types.TextContent(type="text", text=resposta)]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ Erro ao verificar status: {str(e)}"
            )]

    async def run(self):
        """Executa o servidor MCP"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="tribunal-mcp",
                    server_version="1.0.0",
                    capabilities=ServerCapabilities(
                        tools={}
                    ),
                ),
            )

async def main():
    """Função principal"""
    server = TribunalMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

