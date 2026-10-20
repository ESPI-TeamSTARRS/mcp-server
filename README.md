# bm25-mcp

Standalone MCP server exposing a BM25 keyword search over a documentation folder (`.md` / `.txt`, `actions-taken/` excluded). The index follows the files on disk: no restart needed after an edit.

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
| `uv run poe check` | Enchaîne toutes les vérifications (aujourd'hui : `test`) ; appelée par le hook `pre-push` |

Les tâches `lint`, `typecheck`, `cov` ou `ingest` n'existent pas : le dépôt n'a ni ruff, ni mypy, ni pytest-cov, ni étape d'ingestion (l'index BM25 suit les fichiers sur disque). Ajoutez-les à `[tool.poe.tasks]` et à la séquence `check` le jour où l'outil est installé.
