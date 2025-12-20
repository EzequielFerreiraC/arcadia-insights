"""
Choice Entity - Domain Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from a_configs.database import Base


class Choice(Base):
    """Choice entity"""
    __tablename__ = "choices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False, index=True)
    save_id = Column(UUID(as_uuid=True), ForeignKey("saves.id"), nullable=False, index=True)
    episode = Column(Integer, nullable=False, index=True)
    chapter = Column(Integer, nullable=False)
    choice_id = Column(String(100), nullable=False, index=True)
    choice_text = Column(String(500), nullable=False)
    option_selected = Column(String(200), nullable=False)
    timestamp_in_game = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Choice(id={self.id}, episode={self.episode}, choice_id={self.choice_id})>"
