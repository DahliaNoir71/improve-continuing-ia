from pydantic import BaseModel

class DataPointOut(BaseModel):
    id: int
    generation_id: int
    x1: float
    x2: float
    label: int

    class Config:
        orm_mode = True
