#!/usr/bin/env python3
"""Delete saves stuck in 'processing' (leftovers from before the Kafka fix)."""
from __future__ import annotations

import sys

import requests

API = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

saves = requests.get(f"{API}/api/v1/saves/?limit=100", timeout=10).json()
stuck = [s for s in saves if s.get("status") == "processing"]
print(f"{len(stuck)} save(s) presos em 'processing'.")

for s in stuck:
    r = requests.delete(f"{API}/api/v1/saves/{s['id']}", timeout=10)
    print(f"  delete {s['filename']} ({s['id'][:8]}) -> {r.status_code}")

print("Concluído.")
