Local setup

```sh
  # Update YOUR_API_KEY and YOUR_PROJECT_ID in dockercompose.yml

  # First run with migration ennabled
  RUN_MIGRATION=1 docker compose -f dockercompose.yml up --build 

  # From the second time, just need to run up --build
  docker compose -f dockercompose.yml up --build 
```

Run local LLM model
```sh
  # download Ollama at https://ollama.com/download
  
  # run llama3.1 model (good for testing on local)
  ollama run llama3.1
```

Run MCP client

- pipx install poetry
- For tts usage: install any player mpv | mpg123 | aplay

```sh
cd src/projects/host_chat

poetry install

export FINDXAI_MCP_CONNECTION=http://localhost:8080/sse  
export TTS_REST_CONNECTION=http://localhost:8081

# For debug
export DEBUG=1

python main.py

```

For remote MCP server

```sh
export FINDXAI_MCP_CONNECTION=[http/https]://<ip>:<port>/sse  
```