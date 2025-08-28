import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "dbs" / f"main.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

#cur.execute("DROP TABLE EndPointsURLs")
cur.execute('''
CREATE TABLE IF NOT EXISTS EndPointsURLs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  method TEXT NOT NULL CHECK(method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE'))
);
''')

conn.commit()
conn.close()