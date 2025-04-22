import sys
import time
import threading
import itertools
import asyncio
import json
import os

from mcp import types
from typing import Optional

from dotenv import load_dotenv
from mcp.types import TextContent

from mcp_client import FindxAiClient
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, FunctionMessage

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from tool_play_audio import PlayBase64AudioTool

load_dotenv()  # load environment variables from .env

class ChatHostClient:
    def __init__(self):
        self.findxai_client = FindxAiClient()
        self.ollama = ChatOllama(
            model="llama3.1:latest",
        )
        self.agent: Optional[CompiledGraph] = None

    async def connect_mcp_servers(self):
        """Connect to mcp servers"""
        await self.findxai_client.connect_to_server()
        tools = await load_mcp_tools(self.findxai_client.get_session())
        self.agent = create_react_agent(
            self.ollama,
            tools=tools,
            prompt="""
                You are a helpful assistant. 
                You have access to a set of tools (each with its own name and description). 
                ▶️ Only invoke a tool when the user explicitly needs something *you cannot do yourself*—for example, real‑time web searches, database lookups, or actions on external systems. Always add a date filter and human's query for tools that support it.
                ▶️ If the user’s question can be answered from your own knowledge (e.g. definitions, calculations, general explanations), respond directly in Vietnamese *without* calling any tool.  
                ▶️ When you do call a tool, use exactly the tool’s name and pass its arguments as specified, then wait for its output before continuing your answer.
            """
        )

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
        os.getenv("DEBUG", "0") == "1" and print(f"Response: {response}")

        stop_event.set()
        spin_thread.join()
        first_chunk = False

        # 2) normalize into a list of messages: used for tool_messages only
        if isinstance(response, dict) and "messages" in response:
            tool_messages = response["messages"]
        else:
            tool_messages = [response]
        
        for msg in tool_messages:
            # msg has tool_calls in additional_kwargs
            tool_calls = msg.additional_kwargs.get("tool_calls", [])
            if isinstance(msg, AIMessage) and len(tool_calls) > 0:
                if tool_calls[0]["function"]["name"] == "convert_text_to_speech_and_play_audio":
                    args = json.loads(tool_calls[0]["function"]["arguments"])
                    os.getenv("DEBUG", "0") == "1" and print(f"Args for convert_text_to_speech_and_play_audio: {args}")
                    play_base64_audio = PlayBase64AudioTool()
                    result = play_base64_audio.run({"text": args["text"], "language": args["language"]})
            # msg has direct tool calls field
            tool_calls = getattr(msg, "tool_calls", [])
            if isinstance(msg, AIMessage) and len(tool_calls) > 0:
                if tool_calls[0]["name"] == "convert_text_to_speech_and_play_audio":
                    args = tool_calls[0]["args"]
                    os.getenv("DEBUG", "0") == "1" and print(f"Args for convert_text_to_speech_and_play_audio: {args}")
                    play_base64_audio = PlayBase64AudioTool()
                    result = play_base64_audio.run({"text": args["text"], "language": args["language"]})


        if "messages" in response:
            messages = response["messages"]
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    print(msg.content)
                break

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
