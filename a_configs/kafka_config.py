"""
Kafka Configuration
"""
import json
from typing import Dict, Any
from a_configs.settings import get_settings

settings = get_settings()


def get_producer_config() -> Dict[str, Any]:
    """Get Kafka producer configuration"""
    return {
        "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "acks": "all",
        "compression_type": "gzip",
        "max_in_flight_requests_per_connection": 5,
        "retries": 3,
        # Serialize event dicts to JSON bytes (consumers use json.loads).
        "value_serializer": lambda v: json.dumps(v, default=str).encode("utf-8"),
    }


def get_consumer_config(group_id: str) -> Dict[str, Any]:
    """Get Kafka consumer configuration"""
    return {
        "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "group_id": group_id,
        "auto_offset_reset": "earliest",
        "enable_auto_commit": True,
        "max_poll_records": 500,
    }


# Topic configurations
TOPICS = {
    "saves_uploaded": settings.KAFKA_TOPIC_SAVES_UPLOADED,
    "choices_extracted": settings.KAFKA_TOPIC_CHOICES_EXTRACTED,
    "events_domain": settings.KAFKA_TOPIC_EVENTS_DOMAIN,
}
