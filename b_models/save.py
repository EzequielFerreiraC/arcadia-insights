"""
Save File Models - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, UUID4
from enum import Enum


class SaveStatus(str, Enum):
    """Save processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class SaveUpload(BaseModel):
    """Schema for uploading a save file"""
    player_id: UUID4
    filename: str = Field(..., min_length=1, max_length=255)
    file_size_bytes: int = Field(..., gt=0)
    checksum: str = Field(..., description="MD5 checksum")


class SaveResponse(BaseModel):
    """Schema for save response"""
    id: UUID4
    player_id: UUID4
    filename: str
    file_size_bytes: int
    checksum: str
    status: SaveStatus
    s3_path: Optional[str] = None
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    choices_extracted: int = 0
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class SaveProcessingResult(BaseModel):
    """Schema for save processing result"""
    save_id: UUID4
    status: SaveStatus
    choices_count: int
    processing_time_seconds: float
    error_message: Optional[str] = None
