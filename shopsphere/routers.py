APP_DB_MAP = {
  "default": ["dovix", "auth", "token_blacklist", "admin", "contenttypes", "sessions", ],
  "core": ["authentication", "clients", "administrators", ],
  "main": ["core", ],
}

APP_TO_DB = {}
for db, apps in APP_DB_MAP.items():
  for app in apps:
    APP_TO_DB[app] = db
DBS_SET = set(APP_DB_MAP.keys())
class DbRouter:
  def db_for_read(self, model, **hints):
    db = APP_TO_DB.get(model._meta.app_label)
    print(f"📖 [READ] App: {model._meta.app_label} | Model: {model.__name__} → DB: {db}")
    return db
  def db_for_write(self, model, **hints):
    db = APP_TO_DB.get(model._meta.app_label)
    print(f"✏️ [WRITE] App: {model._meta.app_label} | Model: {model.__name__} → DB: {db}")
    return db
  def allow_relation(self, obj1, obj2, **hints):
    db1 = obj1._state.db
    db2 = obj2._state.db
    allowed = db1 in DBS_SET and db2 in DBS_SET
    status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
    print(f"🔗 [RELATION] {obj1.__class__.__name__} ({db1}) ↔ {obj2.__class__.__name__} ({db2}) → {status}")
    return True if allowed else None
  def allow_migrate(self, db, app_label, **hints):
    allowed_apps = APP_DB_MAP.get(db, [])
    should_migrate = app_label in allowed_apps
    status = "✅ YES" if should_migrate else "❌ NO"
    print(f"🛠️ [MIGRATE] App: {app_label} → DB: {db} | Allowed: {status}")
    return should_migrate if app_label in APP_TO_DB else None
