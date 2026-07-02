from pydantic import BaseModel

class RejectDatasetRequest(BaseModel):
    comment: str