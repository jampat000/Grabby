from app.log_sanitize import redact_url_for_logging


def test_redacts_api_key_query() -> None:
    u = "http://localhost:8096/Items?api_key=SECRET123&Limit=1"
    assert "SECRET123" not in redact_url_for_logging(u)
    assert "api_key=***" in redact_url_for_logging(u) or "***" in redact_url_for_logging(u)


def test_redacts_userinfo() -> None:
    u = "http://user:pass@host:8096/path"
    out = redact_url_for_logging(u)
    assert "user" not in out
    assert "pass" not in out
    assert "host:8096" in out
