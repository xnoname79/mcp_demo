import os

from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.sse import sse_client

class FindxAiClient:
  def __init__(self):
      self.session: Optional[ClientSession] = None
      self.exit_stack = AsyncExitStack()

  
  async def connect_to_server(self):
    """Connect to an FindxAI SSE server
        
    Args:
        server_script_path: Path to the server script (.py or .js)
    """
        
    target = os.getenv("FINDXAI_MCP_CONNECTION")
    sse_transport = await self.exit_stack.enter_async_context(sse_client(target))
    self.read, self.write = sse_transport
    self.session = await self.exit_stack.enter_async_context(ClientSession(self.read, self.write))
        
    await self.session.initialize()
        
    # List available tools
    response = await self.session.list_tools()
    tools = response.tools
    print("\nConnected to findxai mcp with tools:", [tool.name for tool in tools])

  async def list_tools(self) -> types.ListToolsResult:
    response = await self.session.list_tools()
    return response.tools

  async def call_tool(self, name: str, args: dict[str, any]) -> types.CallToolResult:
    return await self.session.call_tool(name, args)
  
  def get_server_name(self) -> str:
    return "findxai"

  async def cleanup(self):
    await self.exit_stack.aclose()