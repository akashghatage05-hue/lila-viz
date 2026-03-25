import json
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import pyarrow.parquet as pq


PLAYER_DATA_DIR = Path("player_data")
OUTPUT_EVENTS_FILE = Path("public/data.json")
OUTPUT_MATCHES_FILE = Path("public/matches.json")
TARGET_COLUMNS = ["user_id", "match_id", "map_id", "x", "y", "z", "ts", "event"]


UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)


def to_utf8_string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def to_timestamp_ms(value: Any) -> int:
    if value is None:
        return 0

    if isinstance(value, (int, float)):
        return int(value)

    if hasattr(value, "timestamp"):
        # datetime-like object
        return int(value.timestamp() * 1000)

    # pyarrow TimestampScalar often supports cast/str conversion;
    # try string parse last.
    text = str(value)
    if text.isdigit():
        return int(text)
    try:
        from datetime import datetime

        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except ValueError:
        return 0


def is_bot_user(user_id: str) -> bool:
    if not user_id:
        return False

    if user_id.isdigit() and len(user_id) <= 8:
        return True

    if UUID_RE.match(user_id):
        return False

    try:
        uuid.UUID(user_id)
        return False
    except (ValueError, AttributeError, TypeError):
        return user_id.isdigit()


def read_parquet_rows(file_path: Path) -> List[Dict[str, Any]]:
    table = pq.read_table(file_path, columns=TARGET_COLUMNS)
    return table.to_pylist()


def main() -> None:
    if not PLAYER_DATA_DIR.exists():
        raise FileNotFoundError(f"Folder not found: {PLAYER_DATA_DIR}")

    date_dirs = sorted(
        [p for p in PLAYER_DATA_DIR.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )

    all_events: List[Dict[str, Any]] = []
    unique_players: Set[str] = set()
    match_stats: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

    for date_dir in date_dirs:
        files = sorted([p for p in date_dir.rglob("*") if p.is_file()])
        print(f"Processing {date_dir.name}... {len(files)} files")

        for file_path in files:
            try:
                rows = read_parquet_rows(file_path)
            except Exception as exc:
                print(f"  Skipping unreadable file {file_path}: {exc}")
                continue

            for row in rows:
                user_id = to_utf8_string(row.get("user_id"))
                match_id = to_utf8_string(row.get("match_id"))
                map_id = to_utf8_string(row.get("map_id"))
                event_text = to_utf8_string(row.get("event"))
                ts_ms = to_timestamp_ms(row.get("ts"))
                bot = is_bot_user(user_id)

                event_obj = {
                    "user_id": user_id,
                    "match_id": match_id,
                    "map_id": map_id,
                    "x": row.get("x"),
                    "y": row.get("y"),
                    "z": row.get("z"),
                    "ts": ts_ms,
                    "event": event_text,
                    "is_bot": bot,
                    "date": date_dir.name,
                }
                all_events.append(event_obj)

                if user_id:
                    unique_players.add(user_id)

                match_key = (match_id, map_id, date_dir.name)
                if match_key not in match_stats:
                    match_stats[match_key] = {
                        "match_id": match_id,
                        "map_id": map_id,
                        "date": date_dir.name,
                        "human_users": set(),
                        "bot_count": 0,
                    }

                if bot:
                    match_stats[match_key]["bot_count"] += 1
                else:
                    if user_id:
                        match_stats[match_key]["human_users"].add(user_id)

    matches_output = []
    for data in match_stats.values():
        matches_output.append(
            {
                "match_id": data["match_id"],
                "map_id": data["map_id"],
                "date": data["date"],
                "player_count": len(data["human_users"]),
                "bot_count": data["bot_count"],
            }
        )

    OUTPUT_EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_EVENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False)

    with OUTPUT_MATCHES_FILE.open("w", encoding="utf-8") as f:
        json.dump(matches_output, f, ensure_ascii=False)

    print("Done.")
    print(f"Total events: {len(all_events)}")
    print(f"Unique matches: {len(matches_output)}")
    print(f"Unique players: {len(unique_players)}")


if __name__ == "__main__":
    main()
