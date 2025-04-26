Local setup

```sh
  # Get {YOUR_GOOGLE_API_KEY} at https://console.cloud.google.com/apis/credentials
    # Tips: Restrict the API key so it can only access the Google Custom Search API.

  # Create and get {YOUR_SEARCH_ENGINE_PROJECT_ID} at https://programmablesearchengine.google.com/controlpanel/all
    # Tips: Add the NewsArticle schema to the page restrictions so you only retrieve articles.
  
  # First run with migration ennabled
  RUN_MIGRATION=1 \
  API_KEY={YOUR_GOOGLE_API_KEY} \
  PROJECT_ID={YOUR_SEARCH_ENGINE_PROJECT_ID} \
  docker compose -f dockercompose.yml up --build 

  # From the second time, just need to run up --build
  docker compose -f dockercompose.yml up --build 
```

Run local LLM model
```sh
  # download Ollama at https://ollama.com/download
  
  # run qwen2.5:3b model (good for testing on local)
  ollama run qwen2.5:3b
```

Run MCP client

- pipx install poetry
- For tts usage: install any player mpv | mpg123 | aplay

```sh
cd src/projects/host_chat

poetry install

# LLM models
  # ollama/qwen2.5:3b
  # openai/gpt-4o-mini

# For debug
export DEBUG=1

# For Open AI models
export OPEN_AI_API={YOUR_API}

FINDXAI_MCP_CONNECTION=http://localhost:8080/sse \
TTS_REST_CONNECTION=http://localhost:8081 \
REDIS_URL=redis://localhost:6379?db=3 \
LLM_MODEL=ollama/qwen2.5:3b \
python main.py

```

For remote MCP server

```sh
export FINDXAI_MCP_CONNECTION=[http/https]://<ip>:<port>/sse  
```