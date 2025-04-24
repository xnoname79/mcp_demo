Local setup

```sh
  # First run with migration ennabled
  RUN_MIGRATION=1 \
  API_KEY={YOUR_API_KEY} \
  PROJECT_ID={YOUR_PROJECT_ID} \
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

export FINDXAI_MCP_CONNECTION=http://localhost:8080/sse  
export TTS_REST_CONNECTION=http://localhost:8081
export REDIS_URL=redis://localhost:6379?db=3

# For debug
export DEBUG=1

python main.py

```

For remote MCP server

```sh
export FINDXAI_MCP_CONNECTION=[http/https]://<ip>:<port>/sse  
```