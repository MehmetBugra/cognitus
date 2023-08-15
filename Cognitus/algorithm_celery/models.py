from sqlalchemy import Column, Integer, String
from database import Base


class DataModel(Base):
    __tablename__ = "prediction_datamodel"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    label = Column(String)
