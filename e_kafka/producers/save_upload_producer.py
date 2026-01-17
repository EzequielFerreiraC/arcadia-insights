"""
Save Upload Event Producer
Publishes events when save files are uploaded
"""
import json
import logging
from typing import Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError

from a_configs.kafka_config import get_producer_config, TOPICS
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class SaveUploadProducer:
    """Producer for save upload events"""

    def __init__(self):
        self.producer = None
        self.topic = TOPICS['saves_uploaded']

    def connect(self):
        """Initialize Kafka producer connection"""
        try:
            config = get_producer_config()
            self.producer = KafkaProducer(**config)
            logger.info(f"Connected to Kafka, topic: {self.topic}")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise

    def send_save_uploaded_event(
        self,
        save_id: str,
        player_id: str,
        filename: str,
        file_size_bytes: int,
        checksum: str,
        s3_path: str
    ) -> bool:
        """
        Send save uploaded event to Kafka

        Args:
            save_id: UUID of the save
            player_id: UUID of the player
            filename: Original filename
            file_size_bytes: File size in bytes
            checksum: MD5 checksum
            s3_path: S3 storage path

        Returns:
            bool: True if sent successfully
        """
        if not self.producer:
            self.connect()

        event = {
            'event_type': 'save.uploaded',
            'save_id': save_id,
            'player_id': player_id,
            'filename': filename,
            'file_size_bytes': file_size_bytes,
            'checksum': checksum,
            's3_path': s3_path,
            'timestamp': None  # Will be set by Kafka
        }

        try:
            future = self.producer.send(
                self.topic,
                value=event,
                key=save_id.encode('utf-8')
            )
            
            # Wait for the send to complete
            metadata = future.get(timeout=10)
            
            logger.info(
                f"Save uploaded event sent: save_id={save_id}, "
                f"partition={metadata.partition}, offset={metadata.offset}"
            )
            return True

        except KafkaError as e:
            logger.error(f"Failed to send save uploaded event: {e}")
            return False

    def close(self):
        """Close Kafka producer connection"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


# Singleton instance
_producer_instance = None


def get_save_upload_producer() -> SaveUploadProducer:
    """Get or create save upload producer instance"""
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = SaveUploadProducer()
    return _producer_instance
