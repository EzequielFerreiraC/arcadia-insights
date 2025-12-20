"""
Player Entity - Domain Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from a_configs.database import Base
import enum


class PlatformEnum(str, enum.Enum):
    """Gaming platform enum"""
    PC = "PC"
    PLAYSTATION = "PlayStation"
    XBOX = "Xbox"
    NINTENDO = "Nintendo"


class Player(Base):
    """Player entity"""
    __tablename__ = "players"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country = Column(String(2), nullable=False, index=True)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    game_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    total_saves = Column(Integer, default=0, nullable=False)
    total_choices = Column(Integer, default=0, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Player(id={self.id}, country={self.country}, platform={self.platform})>"
