# bm25-mcp

Standalone MCP server, used by the `Chatbot-Rag` API (`../Chatbot-Rag`), which **needs it up** to find the procedure matching an incident. It exposes a BM25 keyword search over a documentation folder (`.md` / `.txt`, `actions-taken/` excluded). The index follows the files on disk: no restart needed after an edit.

Start it **before** the RAG API: the API reaches it on `http://localhost:8001/mcp`, and every diagnosis fails with `502` while it is down.

## Tool

`search_docs(query: str, limit: int = 5)` → list of `{path, text, score}`, most relevant first (`limit` is capped at 20).

## Configuration

| Variable | Description |
|---|---|
| `DEBUG` | Print `[DEBUG]` logs on stdout (default `false`) |
| `DOCS_PATH` | Documentation folder (default `documentations`) |
| `HOST` | HTTP bind address (default `0.0.0.0`) |
| `PORT` | HTTP port (default `8001`) |
| `MCP_TRANSPORT` | `streamable-http` (default, endpoint `/mcp`), `sse` or `stdio` |

## Run

### With Docker (what the RAG API expects)

```bash
cp .env.exemple .env      # set DOCS_PATH to the documentation folder to index (e.g. ../Chatbot-Rag/documentations)
docker compose up --build -d
curl http://localhost:8001/health                # {"status":"ok"}
```

The documentation folder is mounted read-only at `/app/documentations` and port 8001 is published on the host.  `docker-compose.yml` only passes `DOCS_PATH` to the container, so `HOST`, `PORT` and `MCP_TRANSPORT` from `.env` only apply without Docker. Documents added or edited on the host are indexed on the next search, no restart needed.

### Without Docker

```bash
uv run bm25-mcp                                  # http://localhost:8001/mcp
MCP_TRANSPORT=stdio uv run bm25-mcp              # for a local MCP client
uv run poe serve                                 # same as uv run bm25-mcp
curl http://localhost:8001/health                # {"status":"ok"} (HTTP transports only)
```

# Initialisation des hooks Git
Pour initialiser les hooks, executez la commande suivante :
```bash
git config core.hooksPath "git-hooks"
```


## Développement

Les tâches sont lancées avec [Poe the Poet](https://poethepoet.natn.io/) via uv (`uv run poe --help` les liste) :

| Commande | Description |
|---|---|
| `uv run poe test` | Lance la suite de tests (pytest) |
| `uv run poe serve` | Démarre le serveur MCP BM25 (configuration via `.env`) |
| `uv run poe check` | Toutes les vérifications de la CI : ruff (lint + format), mypy, tests avec couverture ≥ 80 % ; appelée par le hook `pre-push` |
| `uv run poe audit` | `pip-audit` sur les dépendances d'exécution |

Hooks Git : `uv run pre-commit install --hook-type pre-commit --hook-type commit-msg` (ruff, gitleaks, message de commit).
