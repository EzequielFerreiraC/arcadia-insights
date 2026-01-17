"""
Choice Extracted Event Producer
Publishes events when choices are extracted from save files
"""
import json
import logging
from typing import Dict, Any, List
from kafka import KafkaProducer
from kafka.errors import KafkaError

from a_configs.kafka_config import get_producer_config, TOPICS
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class ChoiceExtractedProducer:
    """Producer for choice extraction events"""

    def __init__(self):
        self.producer = None
        self.topic = TOPICS['choices_extracted']

    def connect(self):
        """Initialize Kafka producer connection"""
        try:
            config = get_producer_config()
            self.producer = KafkaProducer(**config)
            logger.info(f"Connected to Kafka, topic: {self.topic}")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise

    def send_choices_extracted_event(
        self,
        save_id: str,
        player_id: str,
        choices: List[Dict[str, Any]],
        total_choices: int
    ) -> bool:
        """
        Send choices extracted event to Kafka

        Args:
            save_id: UUID of the save
            player_id: UUID of the player
            choices: List of extracted choice dictionaries
            total_choices: Total number of choices extracted

        Returns:
            bool: True if sent successfully
        """
        if not self.producer:
            self.connect()

        event = {
            'event_type': 'choices.extracted',
            'save_id': save_id,
            'player_id': player_id,
            'choices': choices,
            'total_choices': total_choices,
            'timestamp': None
        }

        try:
            future = self.producer.send(
                self.topic,
                value=event,
                key=save_id.encode('utf-8')
            )
            
            metadata = future.get(timeout=10)
            
            logger.info(
                f"Choices extracted event sent: save_id={save_id}, "
                f"total_choices={total_choices}, "
                f"partition={metadata.partition}, offset={metadata.offset}"
            )
            return True

        except KafkaError as e:
            logger.error(f"Failed to send choices extracted event: {e}")
            return False

    def close(self):
        """Close Kafka producer connection"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


# Singleton instance
_producer_instance = None


def get_choice_extracted_producer() -> ChoiceExtractedProducer:
    """Get or create choice extracted producer instance"""
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = ChoiceExtractedProducer()
    return _producer_instance
