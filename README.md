Local setup

```sh
  docker compose -f dockercompose.yml up
```
Connect db and run migration findxai.session.sql

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
export FINDXAI_MCP_CONNECTION=http://<service>:<port>/sse  
```