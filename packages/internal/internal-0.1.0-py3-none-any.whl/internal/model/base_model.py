from datetime import datetime

from pydantic import BaseModel, Field


class InternalBaseModel(BaseModel):
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime = Field(default_factory=datetime.utcnow)
