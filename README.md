Local setup

```sh
  # Update YOUR_API_KEY and YOUR_PROJECT_ID in dockercompose.yml
  docker compose -f dockercompose.yml up --build 
```
Connect db and run migration findxai.session.sql

Run local LLM model
```sh
  # download Ollama at https://ollama.com/download
  
  # run llama3.1 model (good for testing on local)
  ollama run llama3.1
```

Run MCP client

- pipx install poetry

```sh
cd src/projects/host_chat

poetry install

export FINDXAI_MCP_CONNECTION=http://localhost:8080/sse  

python main.py

```

For remote MCP server

```sh
export FINDXAI_MCP_CONNECTION=[http/https]://<ip>:<port>/sse  
```