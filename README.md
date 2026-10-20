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
uv run pytest
```
# Initialisation des hooks Git
Pour initialiser les hooks, executez la commande suivante :
```bash
git config core.hooksPath "git-hooks"
```

