import sqlite3, uuid
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "dbs" / "core.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON") 
cur = conn.cursor()

#cur.execute("DROP TABLE users")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  user_id INTEGER UNIQUE,
  telegram_user_id BIGINT UNIQUE,
  balance BIGINT DEFAULT 0,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
  actived_account BOOLEAN DEFAULT 0,
  preferred_language TEXT DEFAULT 'en' CHECK (preferred_language IN ('en', 'ar')),
  joined_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")


conn.commit()
conn.close()

print(f"✅ تم إنشاء قاعدة البيانات في: {DB_PATH}")
