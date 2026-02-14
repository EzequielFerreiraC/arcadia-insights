"""Smoke test: import the FastAPI app and list routes without starting a server."""
import importlib
import os
import sys

# Ensure the repo root (parent of l_scripts/) is importable.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

mods = ["fastapi", "sqlalchemy", "asyncpg", "minio", "kafka", "pydantic_settings"]
missing = []
for m in mods:
    try:
        importlib.import_module(m)
    except Exception as exc:  # noqa: BLE001
        missing.append(f"{m}: {exc}")

if missing:
    print("MISSING_DEPS")
    for x in missing:
        print("  -", x)
    sys.exit(2)

print("deps OK")

try:
    from c_api.src.main import app
except Exception as exc:  # noqa: BLE001
    import traceback
    print("IMPORT_APP_FAILED")
    traceback.print_exc()
    sys.exit(3)

routes = sorted(
    f"{','.join(sorted(r.methods))} {r.path}"
    for r in app.routes
    if getattr(r, "methods", None)
)
print(f"APP_OK routes={len(routes)}")
for r in routes:
    print("  ", r)

print("ALL_ROUTES:")
for r in app.routes:
    print("  ", type(r).__name__, getattr(r, "path", getattr(r, "path_format", "?")))
