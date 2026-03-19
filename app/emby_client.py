from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class EmbyConfig:
    base_url: str
    api_key: str


class EmbyClient:
    def __init__(self, cfg: EmbyConfig, *, timeout_s: float = 30.0) -> None:
        self._client = httpx.AsyncClient(
            base_url=cfg.base_url.rstrip("/"),
            # Emby installs vary in how they validate API credentials; send
            # both common token headers and api_key query param for compatibility.
            headers={
                "X-Emby-Token": cfg.api_key,
                "X-MediaBrowser-Token": cfg.api_key,
            },
            params={"api_key": cfg.api_key},
            timeout=timeout_s,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def health(self) -> bool:
        # Simple health/probe endpoint.
        r = await self._client.get("/System/Info")
        r.raise_for_status()
        return True

    async def users(self) -> list[dict]:
        r = await self._client.get("/Users")
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []

    async def items_for_user(self, *, user_id: str, limit: int) -> list[dict]:
        # Pull only top-level Movie and Series so we do not delete episodes directly.
        # Recursive scans libraries and returns metadata including UserData.
        params = {
            "Recursive": "true",
            "IncludeItemTypes": "Movie,Series",
            "Fields": "UserData,DateCreated,PremiereDate,DateLastMediaAdded",
            "SortBy": "DateCreated",
            "SortOrder": "Descending",
            "StartIndex": "0",
            "Limit": str(max(1, min(5000, int(limit)))),
        }
        r = await self._client.get(f"/Users/{user_id}/Items", params=params)
        r.raise_for_status()
        payload = r.json()
        items = payload.get("Items") if isinstance(payload, dict) else None
        return items if isinstance(items, list) else []

    async def delete_item(self, item_id: str) -> None:
        # Emby delete endpoint.
        r = await self._client.delete(f"/Items/{item_id}")
        r.raise_for_status()
