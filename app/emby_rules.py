from __future__ import annotations

from datetime import UTC, datetime


def parse_iso_dt(raw: str | None) -> datetime | None:
    if not raw or not isinstance(raw, str):
        return None
    value = raw.strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def days_since(item: dict) -> int | None:
    for key in ("DateLastMediaAdded", "DateCreated", "PremiereDate"):
        dt = parse_iso_dt(item.get(key))
        if dt is not None:
            return max(0, int((datetime.now(UTC) - dt).total_seconds() // 86400))
    return None


def emby_rating(user_data: dict) -> float | None:
    rating = user_data.get("Rating")
    if isinstance(rating, (int, float)):
        return float(rating)
    return None


def emby_user_played(user_data: dict) -> bool:
    return bool(user_data.get("Played"))


def parse_genres_csv(raw: str | None) -> set[str]:
    if not raw:
        return set()
    out: set[str] = set()
    for chunk in raw.split(","):
        v = chunk.strip().lower()
        if v:
            out.add(v)
    return out


def movie_matches_selected_genres(item: dict, selected_genres: set[str]) -> bool:
    if not selected_genres:
        return True
    genres = item.get("Genres") if isinstance(item.get("Genres"), list) else []
    item_genres = {str(g).strip().lower() for g in genres if str(g).strip()}
    return bool(item_genres & selected_genres)


def evaluate_candidate(
    item: dict,
    *,
    movie_watched_rating_below: int,
    movie_unwatched_days: int,
    tv_delete_watched: bool,
    tv_unwatched_days: int,
) -> tuple[bool, list[str], int | None, float | None, bool]:
    item_type = str(item.get("Type", "") or "").strip()
    is_movie = item_type == "Movie"
    is_tv = item_type in {"Series", "Season", "Episode"}
    if not is_movie and not is_tv:
        return (False, [], None, None, False)

    user_data = item.get("UserData") if isinstance(item.get("UserData"), dict) else {}
    played = emby_user_played(user_data)
    rating = emby_rating(user_data)
    age_days = days_since(item)

    unwatched_days = movie_unwatched_days if is_movie else tv_unwatched_days
    media_label = "movie" if is_movie else "tv"

    reasons: list[str] = []
    if is_movie and movie_watched_rating_below > 0 and played and rating is not None and rating < float(movie_watched_rating_below):
        reasons.append(f"{media_label}: watched and rated {rating:g} < {movie_watched_rating_below}")
    if is_tv and tv_delete_watched and played:
        reasons.append(f"{media_label}: watched")
    if unwatched_days > 0 and (not played) and age_days is not None and age_days >= unwatched_days:
        reasons.append(f"{media_label}: unwatched and age {age_days}d >= {unwatched_days}d")

    return (len(reasons) > 0, reasons, age_days, rating, played)
