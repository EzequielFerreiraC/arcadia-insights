"""
Save Entity - Domain Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from a_configs.database import Base
import enum


class SaveStatusEnum(str, enum.Enum):
    """Save processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Save(Base):
    """Save file entity"""
    __tablename__ = "saves"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    checksum = Column(String(32), nullable=False, unique=True)
    status = Column(SQLEnum(SaveStatusEnum), default=SaveStatusEnum.UPLOADED, nullable=False)
    s3_path = Column(String(500), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    choices_extracted = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Save(id={self.id}, filename={self.filename}, status={self.status})>"
