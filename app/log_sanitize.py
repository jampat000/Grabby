"""Helpers to avoid persisting secrets in user-visible or exported logs."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Query keys that often carry credentials (Emby uses api_key on the wire).
_SENSITIVE_QUERY_KEYS = frozenset(
    {
        "api_key",
        "apikey",
        "token",
        "access_token",
        "refresh_token",
        "key",
        "password",
        "secret",
    }
)


def redact_url_for_logging(url: str | object) -> str:
    """Remove credential-like query params and userinfo from a URL for logging."""
    try:
        p = urlparse(str(url))
        netloc = p.netloc
        if "@" in netloc:
            userinfo, _sep, hostport = netloc.rpartition("@")
            if userinfo and hostport:
                netloc = "***:***@" + hostport
        if not p.query:
            return urlunparse((p.scheme, netloc, p.path, p.params, "", p.fragment))
        pairs = [
            (k, "***" if k.lower() in _SENSITIVE_QUERY_KEYS else v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
        ]
        new_query = urlencode(pairs)
        return urlunparse((p.scheme, netloc, p.path, p.params, new_query, p.fragment))
    except Exception:
        return "<url>"
