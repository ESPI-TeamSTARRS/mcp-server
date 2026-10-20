from pathlib import Path

from bm25_mcp.config import Setting


def clear_env(monkeypatch):
    monkeypatch.setitem(Setting.model_config, "env_file", None)
    for name in ("DEBUG", "DOCS_PATH", "HOST", "PORT", "MCP_TRANSPORT"):
        monkeypatch.delenv(name, raising=False)


def test_defaults(monkeypatch):
    clear_env(monkeypatch)
    setting = Setting()
    assert (setting.DEBUG, setting.DOCS_PATH, setting.HOST, setting.PORT, setting.MCP_TRANSPORT) == (
        False,
        Path("documentations"),
        "0.0.0.0",
        8001,
        "streamable-http",
    )


def test_setting_reads_uppercase_environment_variables(monkeypatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("DOCS_PATH", "/d")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("MCP_TRANSPORT", "stdio")
    setting = Setting()
    assert (str(setting.DOCS_PATH), setting.PORT, setting.MCP_TRANSPORT) == ("/d", 9000, "stdio")


def test_setting_reads_env_file(monkeypatch, tmp_path):
    clear_env(monkeypatch)
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=9100\nDEBUG=true\n")
    monkeypatch.setitem(Setting.model_config, "env_file", env_file)
    setting = Setting()
    assert (setting.PORT, setting.DEBUG) == (9100, True)
