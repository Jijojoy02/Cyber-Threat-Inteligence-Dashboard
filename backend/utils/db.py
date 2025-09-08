import sqlite3, json, os
from datetime import datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS lookups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  indicator TEXT NOT NULL,
  type TEXT,
  vt_positives INTEGER DEFAULT 0,
  vt_total INTEGER DEFAULT 0,
  abuse_score INTEGER DEFAULT 0,
  severity TEXT,
  vt_raw TEXT,
  abuse_raw TEXT,
  created_at TEXT NOT NULL
);
"""

def init_db(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(SCHEMA)
        conn.commit()

def insert_lookup(path: str, row: dict):
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO lookups (indicator, type, vt_positives, vt_total, abuse_score, severity, vt_raw, abuse_raw, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                row.get("indicator"),
                row.get("type"),
                int(row.get("vt_positives") or 0),
                int(row.get("vt_total") or 0),
                int(row.get("abuse_score") or 0),
                row.get("severity"),
                json.dumps(row.get("vt_raw")) if row.get("vt_raw") is not None else None,
                json.dumps(row.get("abuse_raw")) if row.get("abuse_raw") is not None else None,
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        conn.commit()

def fetch_recent(path: str, limit: int = 20):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT id, indicator, type, vt_positives, vt_total, abuse_score, severity, created_at "
            "FROM lookups ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = [dict(r) for r in cur.fetchall()]
    return rows

def get_counts(path: str):
    with sqlite3.connect(path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM lookups")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM lookups WHERE severity='high'")
        high = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM lookups WHERE severity='medium'")
        medium = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM lookups WHERE severity='low'")
        low = cur.fetchone()[0]
    return {"total": total, "high": high, "medium": medium, "low": low}
