import asyncio
import json

from mcp import types
from typing import Optional

from dotenv import load_dotenv
from mcp.types import TextContent

from mcp_client import FindxAiClient
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk, AIMessage

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

import sys
import time
import threading
import itertools

load_dotenv()  # load environment variables from .env

class ChatHostClient:
    def __init__(self):
        self.findxai_client = FindxAiClient()
        self.ollama = ChatOllama(
            model="llama3.1:latest",
        )
        self.agent: Optional[CompiledGraph] = None

        self.available_tools: list[dict[str, any]] = []
        self.tool_server_dict: dict[str, str] = {}

    async def connect_mcp_servers(self):
        """Connect to mcp servers
        """

        await self.findxai_client.connect_to_server()
        tools = await load_mcp_tools(self.findxai_client.get_session())
        self.agent = create_react_agent(
            self.ollama,
            tools=tools,
            prompt="""
                You are a Vietnamese‑language assistant. 
                You have access to a set of tools (each with its own name and description). 
                ▶️ Only invoke a tool when the user explicitly needs something *you cannot do yourself*—for example, real‑time web searches, database lookups, or actions on external systems. Always add a date filter and human's query for tools that support it.
                ▶️ If the user’s question can be answered from your own knowledge (e.g. definitions, calculations, general explanations), respond directly in Vietnamese *without* calling any tool.  
                ▶️ When you do call a tool, use exactly the tool’s name and pass its arguments as specified, then wait for its output before continuing your answer.
            """
        )

        findxai_tools = await self.findxai_client.list_tools()
        for tool in findxai_tools:
            self.available_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
            self.tool_server_dict[tool.name] = self.findxai_client.get_server_name(
            )

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
            raise RuntimeError(
                f"No MCP server for tool '{name}' (got '{server_name}')")
        # note the await
        return await self.findxai_client.call_tool(name=name, args=args)

    async def cleanup(self):
        """Clean up resources"""
        await self.findxai_client.cleanup()

    async def process_query(self, query: str) -> None:
        payload = {"messages": query}

        # Create a local Event for stopping the spinner
        stop_event = threading.Event()

        # Spinner function closes over stop_event
        def spin():
            for c in itertools.cycle("|/-\\"):
                if stop_event.is_set():
                    break
                sys.stdout.write(f"\rWaiting for response... {c}")
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write("\r" + " " * 30 + "\r")  # clear the line

        # Start spinner thread
        spin_thread = threading.Thread(target=spin)
        spin_thread.start()
        
        response = await self.agent.ainvoke(payload)

        stop_event.set()
        spin_thread.join()
        first_chunk = False

        if "messages" in response:
            messages = response["messages"]
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    print(msg.content)

        if isinstance(response, AIMessage):
            print(response.content)

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
