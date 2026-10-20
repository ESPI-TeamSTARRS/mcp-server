import asyncio

from starlette.testclient import TestClient

from bm25_mcp.config import settings
from bm25_mcp.server import MAX_LIMIT, build_server, main


def make_docs(tmp_path, count=1):
    for i in range(count):
        (tmp_path / f"redis{i}.md").write_text(f"# Redis {i}\n\nRestart the redis sentinel.\n")
    return tmp_path


def call_search(docs, **arguments):
    _, structured = asyncio.run(build_server(docs).call_tool("search_docs", arguments))
    return structured["result"]


def test_search_docs_tool_is_exposed(tmp_path):
    tools = asyncio.run(build_server(tmp_path).list_tools())
    assert [tool.name for tool in tools] == ["search_docs"]


def test_search_docs_returns_path_text_and_score(tmp_path):
    hits = call_search(make_docs(tmp_path), query="redis sentinel")
    assert set(hits[0]) == {"path", "text", "score"}
    assert hits[0]["path"] == "redis0.md" and "Restart the redis sentinel." in hits[0]["text"]


def test_no_match_returns_empty_list(tmp_path):
    assert call_search(make_docs(tmp_path), query="kubernetes") == []


def test_default_limit_is_five(tmp_path):
    assert len(call_search(make_docs(tmp_path, 8), query="redis")) == 5


def test_limit_is_capped_and_floored(tmp_path):
    docs = make_docs(tmp_path, MAX_LIMIT + 5)
    assert len(call_search(docs, query="redis", limit=1000)) == MAX_LIMIT
    assert len(call_search(docs, query="redis", limit=0)) == 1


def test_health_endpoint_returns_ok(tmp_path):
    app = build_server(tmp_path).streamable_http_app()
    response = TestClient(app).get("/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"}


def test_main_rejects_missing_docs_folder(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(settings, "DOCS_PATH", tmp_path / "absent")
    assert main() == 2
    assert "DOCS_PATH" in capsys.readouterr().err
