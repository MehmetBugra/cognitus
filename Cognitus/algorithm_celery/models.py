from sqlalchemy import Column, Integer, String
from database import Base


class DataModel(Base):
    __tablename__ = "prediction_datamodel"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    label = Column(String)

class LogModel(Base):
    __tablename__ = "prediction_log"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    accuracy = Column(String)
    started_date = Column(String)
    finished_date = Column(String)
