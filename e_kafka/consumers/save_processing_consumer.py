"""
Save Processing Consumer
Consumes save upload events and triggers processing
"""
import json
import logging
from typing import Callable, Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from a_configs.kafka_config import get_consumer_config, TOPICS
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class SaveProcessingConsumer:
    """Consumer for save upload events"""

    def __init__(self, group_id: str = "save-processing-group"):
        self.consumer = None
        self.group_id = group_id
        self.topic = TOPICS['saves_uploaded']
        self.running = False

    def connect(self):
        """Initialize Kafka consumer connection"""
        try:
            config = get_consumer_config(self.group_id)
            self.consumer = KafkaConsumer(
                self.topic,
                **config
            )
            logger.info(f"Connected to Kafka, topic: {self.topic}, group: {self.group_id}")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise

    def consume(self, callback: Callable[[dict], None], max_messages: Optional[int] = None):
        """
        Consume messages from Kafka and process them

        Args:
            callback: Function to call with each message
            max_messages: Maximum number of messages to consume (None = infinite)
        """
        if not self.consumer:
            self.connect()

        self.running = True
        message_count = 0

        try:
            logger.info(f"Starting to consume from topic: {self.topic}")
            
            for message in self.consumer:
                if not self.running:
                    break

                try:
                    event = message.value
                    logger.info(
                        f"Received save upload event: save_id={event.get('save_id')}, "
                        f"partition={message.partition}, offset={message.offset}"
                    )

                    # Call the processing callback
                    callback(event)

                    message_count += 1
                    if max_messages and message_count >= max_messages:
                        logger.info(f"Reached max messages limit: {max_messages}")
                        break

                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    # Continue processing other messages

        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping consumer")
        finally:
            self.stop()

    def stop(self):
        """Stop consuming and close connection"""
        self.running = False
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")


def process_save_upload(event: dict):
    """
    Example callback to process save upload events
    
    Args:
        event: Save upload event dictionary
    """
    save_id = event.get('save_id')
    s3_path = event.get('s3_path')
    
    logger.info(f"Processing save: {save_id} from {s3_path}")
    
    # TODO: Implement actual processing logic
    # 1. Download save file from S3
    # 2. Parse save file and extract choices
    # 3. Store choices in database
    # 4. Publish choices.extracted event
    # 5. Update save status to 'processed'
    
    logger.info(f"Save processed successfully: {save_id}")
