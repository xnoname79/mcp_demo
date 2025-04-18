import asyncio
import json

from mcp import types

from dotenv import load_dotenv
from mcp.types import TextContent

from mcp_client import FindxAiClient
from open_router import OpenRouter

load_dotenv()  # load environment variables from .env

class ChatHostClient:
    def __init__(self):
        self.findxai_client = FindxAiClient()
        self.open_router = OpenRouter("You are Peter, you will assist user find anything and answer any question for them") 

        self.available_tools: list[dict[str, any]] = []
        self.tool_server_dict: dict[str, str] = {}


    async def connect_mcp_servers(self):
        """Connect to mcp servers
        """

        await self.findxai_client.connect_to_server()
        findxai_tools = await self.findxai_client.list_tools()

        for tool in findxai_tools:
          self.available_tools.append({
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema,
          })
          self.tool_server_dict[tool.name] = self.findxai_client.get_server_name()
    
    def get_server_by_tool(self, tool_name: str) -> str:
        """Get specific mcp client by tool name
        
        Args:
        tool_name: specific name for calling tool
        """
        return self.tool_server_dict[tool_name]

    async def call_tool(self, name: str, args: dict[str, any]) -> types.CallToolResult:
        """Call specific tool with provided mcp client

        Args:
        name: name of tool to be called
        args: parameters passing through the tool
        """
        server_name = self.findxai_client.get_server_name()
        target = self.get_server_by_tool(name)
        if server_name != target:
            raise RuntimeError(f"No MCP server for tool '{name}' (got '{server_name}')")
        # note the await
        return await self.findxai_client.call_tool(name=name, args=args)

    async def cleanup(self):
        """Clean up resources"""
        await self.findxai_client.cleanup()

    async def process_query(self, query: str) -> None:
         # 1. Call your tool
        response = await self.call_tool(name="find_contents", args={"q": query})

        # 2. Extract text content
        if not response or not response.content:
            print("⚠️ No response content received.")
            return

        text = response.content[0].text
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON from tool response.")
            print("Raw content:", text)
            return

        # 3. Extract and print results
        results = data.get("results", [])
        if not results:
            print("⚠️ No search results found.")
            return

        print(f"\n🔎 Top results for: {query}")
        for idx, item in enumerate(results, 1):
            title   = item.get("title", "No title")
            link    = item.get("link", "No link")
            snippet = item.get("snippet", "No snippet")
            print(f"\n{idx}. {title}\n   🔗 {link}\n   📝 {snippet}")

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nChat host client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")

async def main():
    client = ChatHostClient()
    try:
        await client.connect_mcp_servers()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())