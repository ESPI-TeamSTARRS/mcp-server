import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from bm25_mcp.config import settings
from bm25_mcp.logger import logger
from bm25_mcp.search import Bm25DocSearch

DEFAULT_LIMIT = 5
MAX_LIMIT = 20


def build_server(docs_path: Path, host: str = "0.0.0.0", port: int = 8001) -> FastMCP:
    logger.debug(message=f"Building server (docs_path={docs_path}, host={host}, port={port})")
    search = Bm25DocSearch(docs_path)
    mcp = FastMCP("bm25-docs", host=host, port=port)

    @mcp.tool()
    def search_docs(query: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """BM25 keyword search over the incident documentation.

        Pass a short query made of the most distinctive keywords (error names, component names,
        symptoms); strip paths, line numbers and timestamps from stack traces. Returns the full
        content of the best matching documents, most relevant first, as {path, text, score}.
        """
        bounded = max(1, min(limit, MAX_LIMIT))
        logger.debug(message=f"Tool search_docs called (query={query!r}, limit={limit} -> {bounded})")
        hits = search.search(query, bounded)
        logger.debug(
            message=f"Tool search_docs returned {len(hits)} hit(s): "
            + ", ".join(f"{hit.path} ({hit.score:.3f})" for hit in hits)
        )
        return [{"path": hit.path, "text": hit.text, "score": hit.score} for hit in hits]

    return mcp


def main() -> int:
    logger.configure(enabled=settings.DEBUG)
    docs_path = settings.DOCS_PATH
    if not docs_path.is_dir():
        print(f"Configuration error: DOCS_PATH '{docs_path}' is not a directory", file=sys.stderr)
        return 2
    logger.debug(message=f"Starting server with transport {settings.MCP_TRANSPORT}")
    server = build_server(docs_path, host=settings.HOST, port=settings.PORT)
    server.run(transport=settings.MCP_TRANSPORT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
