from pydantic import BaseModel

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: int | None = 100
    overlap_size: int | None = 20
    do_reset: int | None = 0 
