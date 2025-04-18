import httpx
from openai import OpenAI
import os

class OpenRouter:
  def __init__(self, prompt: str):
    self.base_url = "https://openrouter.ai/api/v1" 
    self.api_key = os.getenv("OPENROUTER_API_KEY")
    self.openai_client = OpenAI(
      base_url=self.base_url,
      api_key=self.api_key,
    )    
    self.system_prompt = prompt
  
  async def get_free_models_sorted_by_context_length(self) -> list[dict]:
    """Get all free models and sort models descending by highest context length
    """
    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(self.base_url +"/models", headers=headers, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            free_models = []
            for model in result["data"]:
              if model["pricing"]["prompt"] != "0" or model["pricing"]["completion"] != "0":
                continue
              free_models.append(model)

            # sort in‑place by context_length descending
            free_models.sort(key=lambda m: m["context_length"], reverse=True)
            return free_models
        except Exception:
            return None

    # Filter free models (pricing.prompt == 0 and pricing.completion == 0)

  async def chat(self, message: str, tools: list(dict[str, str])) -> str:
    messages = [
      {
        "role": "sytem",
        "content": self.system_prompt
      },
      {
        "role": "user",
        "content": message
      }
    ]
    # models = await self.get_free_models_sorted_by_context_length()
    # if not models:
    #   raise RuntimeError("No free models found")
    # print(models[0])
    request_1 = {
      "model": "gpt-4.1",
      "messages": messages,
      "tools": tools 
    }
    response_1 = self.openai_client.chat.completions.create(**request_1).message
    print(response_1)


