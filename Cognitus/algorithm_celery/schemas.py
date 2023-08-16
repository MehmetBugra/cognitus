from pydantic import BaseModel

class DataBase(BaseModel):
    label: str
    text: str

class DataSchema(DataBase):
    id: int

class DataDeleteSchema(BaseModel):
    id: int

class DataCreateSchema(DataBase):
    pass

class DataUpdateSchema(DataBase):
    pass

class PredictTextSchema(BaseModel):
    predict_text: str