"""
Object Store (best-effort)
==========================
Fail-safe helper to persist the raw save file into the Bronze bucket (MinIO).
Never raises: storage being down should not fail an upload.
"""
from __future__ import annotations

import io
from datetime import datetime

from a_configs.logging_config import get_logger
from a_configs.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


def put_bronze_save(checksum: str, filename: str, raw: bytes) -> str | None:
    """
    Store the raw save bytes in the Bronze bucket, partitioned by date.
    Returns the `s3://` path on success, or None if storage is unavailable.
    """
    try:
        from a_configs.minio_client import MinIOClient

        client = MinIOClient.get_client()
        date_prefix = datetime.utcnow().strftime("%Y/%m/%d")
        object_key = f"saves/{date_prefix}/{checksum}_{filename}"
        client.put_object(
            settings.MINIO_BUCKET_BRONZE,
            object_key,
            io.BytesIO(raw),
            length=len(raw),
            content_type="application/json",
        )
        path = f"s3://{settings.MINIO_BUCKET_BRONZE}/{object_key}"
        logger.info(f"Save bruto armazenado em {path}")
        return path
    except Exception as exc:  # noqa: BLE001 - best-effort by design
        logger.warning(f"MinIO indisponível (save não armazenado no Bronze): {exc}")
        return None


def get_bronze_object(s3_path: str) -> bytes | None:
    """Download raw bytes from an `s3://bucket/key` path. Returns None on failure."""
    try:
        from a_configs.minio_client import MinIOClient

        client = MinIOClient.get_client()
        without_scheme = s3_path.replace("s3://", "", 1)
        bucket, _, key = without_scheme.partition("/")
        response = client.get_object(bucket, key)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()
    except Exception as exc:  # noqa: BLE001 - best-effort by design
        logger.warning(f"Falha ao ler objeto do Bronze ({s3_path}): {exc}")
        return None
