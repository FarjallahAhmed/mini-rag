

from pydantic import BaseModel, Field, field_validator
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    _id: ObjectId | None = None
    chunk_text: str = Field(...,min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(...,gt=0)
    chunk_object_id: ObjectId





    class Config:
        arbitrary_types_allowed = True