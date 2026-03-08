import json
import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import Any

# Konfigurasi Logging dasar
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

def cetak(teks: str) -> None:
    print(teks, flush=True)

def gen_id() -> str:
    return str(uuid.uuid4())[:8]

def get_wib_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=7)

def safe_json_load(path: str, default: Any):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def safe_json_write(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)