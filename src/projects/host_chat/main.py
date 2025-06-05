import asyncio
import itertools
import json
import os
import sys
import threading
import time

from dotenv import load_dotenv
from hippocampus import Hippocampus
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from mcp_client import FindxAiClient
from tool_play_audio import PlayBase64AudioTool

load_dotenv()  # load environment variables from .env

ROLE_BY_CLASS = {
    HumanMessage: "user",
    AIMessage: "assistant",
}

MODEL_CONTEXT_LENGTH = {
    "ollama/qwen2.5:3b": 128000,
    "openai/gpt-4o-mini": 128000,
}


class ChatHostClient:
    def __init__(self, model: str):
        self.findxai_client = FindxAiClient()
        model_name = model.split("/")[1]
        if "openai" in model:
            self.model = ChatOpenAI(
                model=model_name,
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        elif "ollama" in model:
            self.model = ChatOllama(
                model=model_name,
            )
        self.hippocampus = Hippocampus(MODEL_CONTEXT_LENGTH[model])
        self.agent: CompiledGraph
        print(f"You are using the model: {model}")

    async def connect_mcp_servers(self):
        """Connect to mcp servers"""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379?db=0")
        self.hippocampus.memory_established(redis_url)
        await self.findxai_client.connect_to_server()
        tools = await load_mcp_tools(self.findxai_client.get_session())
        self.agent = create_react_agent(
            self.model,
            tools=tools,
            prompt="""
                You are a helpful assistant. 
                You have access to a set of tools (each with its own name and description). 
                ▶️ Only invoke a tool when the user explicitly needs something *you cannot do yourself*—for example, real‑time web searches, database lookups, or actions on external systems. Always add a date filter and human's query for tools that support it.
                ▶️ If the user’s question can be answered from your own knowledge (e.g. definitions, calculations, general explanations), respond directly in Vietnamese *without* calling any tool.  
                ▶️ When you do call a tool, use exactly the tool’s name and pass its arguments as specified, then wait for its output before continuing your answer.
            """,
        )

    async def cleanup(self):
        """Clean up resources"""
        await self.findxai_client.cleanup()
        self.hippocampus.clear_memory()

    def _handle_tool_calls(self, response):
        # Normalize into a list of messages
        msgs = (
            response.get("messages")
            if isinstance(response, dict) and "messages" in response
            else [response]
        )

        for msg in msgs:
            if not isinstance(msg, AIMessage):
                continue

            tool_calls = msg.additional_kwargs.get("tool_calls", []) or getattr(
                msg, "tool_calls", []
            )
            if not tool_calls:
                continue

            first_call = tool_calls[0]
            name = (
                first_call.get("function", {}).get("name")
                if "function" in first_call
                else first_call.get("name")
            )
            if name != "convert_text_to_speech_and_play_audio":
                continue

            args = {}
            if "function" in first_call:
                args = json.loads(first_call["function"]["arguments"])
            else:
                args = first_call.get("args", {})

            if os.getenv("DEBUG", "0") == "1":
                print(f"Args for {name}: {args}\n")

            player = PlayBase64AudioTool()
            player.run({"text": args["text"], "language": args["language"]})

    def _persist_latest_ai_response(self, response, query):
        """
        Store the latest AIMessage and the triggering user query into memory.
        Works whether `response` is a dict with a 'messages' list or a single AIMessage.
        """
        msgs = (
            response.get("messages")
            if isinstance(response, dict) and "messages" in response
            else [response]
        )

        latest_ai: AIMessage | None = None
        for msg in reversed(msgs):
            if isinstance(msg, AIMessage):
                latest_ai = msg
                break

        if latest_ai:
            self.hippocampus.store_memory("user", query)
            self.hippocampus.store_memory(
                ROLE_BY_CLASS.get(type(latest_ai), "unknown"), latest_ai.content
            )
            print(latest_ai.content)

    async def _process_query(self, query: str) -> None:
        memories = self.hippocampus.recall_memory()
        messages = []
        if memories:
            messages.append(
                SystemMessage(content="Use the memory below to answer accurately.")
            )

        os.getenv("DEBUG", "0") == "1" and print(f"Memories: {memories}\n")
        for turn in memories:
            if turn["role"] == "user":
                messages.append(
                    SystemMessage(
                        content=f"Memory of user's message: {turn['content']}"
                    )
                )
            if turn["role"] == "assistant":
                messages.append(
                    SystemMessage(
                        content=f"Memory of assistant's response: {turn['content']}"
                    )
                )

        messages.append({"role": "user", "content": query})
        payload = {"messages": messages}
        os.getenv("DEBUG", "0") == "1" and print(f"Payload: {payload}\n")

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
        os.getenv("DEBUG", "0") == "1" and print(f"Response: {response}\n")

        stop_event.set()
        spin_thread.join()

        self._handle_tool_calls(response)
        self._persist_latest_ai_response(response, query)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nChat host client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                await self._process_query(query)

            except Exception as e:
                print(f"\nError: {str(e)}")


async def main():
    client = ChatHostClient(os.getenv("LLM_MODEL", "ollama/qwen2.5:3b"))
    try:
        await client.connect_mcp_servers()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())
