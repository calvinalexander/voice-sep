from urllib.parse import non_hierarchical
from pydantic import BaseModel
from typing import Optional


class InferData(BaseModel):
    audio: Optional[str] = None
    file: Optional[str] = None
    fileType: Optional[str] = None


class InferInResponse(BaseModel):
    type: Optional[str] = None
    status: int = 200
    message: str = 'Audio separation success'
    data: Optional[InferData] = None
