from sqlalchemy import Column, Integer, Float
from database.database import Base

class DataPoint(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, index=True)
    x1 = Column(Float)
    x2 = Column(Float)
    label = Column(Integer)