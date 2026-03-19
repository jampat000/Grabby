from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo


DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _parse_hhmm(s: str, *, default: time) -> time:
    try:
        parts = (s or "").strip().split(":")
        if len(parts) != 2:
            return default
        h = int(parts[0])
        m = int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            return default
        return time(hour=h, minute=m)
    except Exception:
        return default


def _parse_days(s: str) -> set[str]:
    # Stored as "Mon,Tue,Wed" etc
    tokens = [t.strip() for t in (s or "").split(",") if t.strip()]
    out = {t for t in tokens if t in DAY_NAMES}
    return out if out else set(DAY_NAMES)


def in_window(
    *,
    schedule_enabled: bool,
    schedule_days: str,
    schedule_start: str,
    schedule_end: str,
    timezone: str = "UTC",
    now: datetime | None = None,
) -> bool:
    """
    Returns True if we're allowed to run *now*.
    Uses timezone (IANA) for day/time; defaults to UTC.

    If start <= end: window is same-day (e.g. 09:00-17:00)
    If start > end: window crosses midnight (e.g. 22:00-02:00)
    """
    if not schedule_enabled:
        return True

    try:
        tz = ZoneInfo(timezone) if timezone else ZoneInfo("UTC")
    except Exception:
        tz = ZoneInfo("UTC")
    now = now or datetime.now(tz)
    if now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    else:
        now = now.astimezone(tz)
    day = DAY_NAMES[now.weekday()]
    allowed_days = _parse_days(schedule_days)
    if day not in allowed_days:
        return False

    start_t = _parse_hhmm(schedule_start, default=time(0, 0))
    end_t = _parse_hhmm(schedule_end, default=time(23, 59))
    cur_t = now.time().replace(second=0, microsecond=0)

    if start_t <= end_t:
        return start_t <= cur_t <= end_t
    # crosses midnight
    return cur_t >= start_t or cur_t <= end_t

