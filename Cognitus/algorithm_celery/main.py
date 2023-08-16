from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import uvicorn

from algorithm import (
    train,
    predict
)

from database import Base, engine, get_db

from crud import ( 
    get_datas,
    get_data,
    create_data,
    update_data,
    delete_data,
    save_file
)
from schemas import (
    DataCreateSchema,
    DataUpdateSchema,
    DataDeleteSchema,
    PredictTextSchema
)


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/train_data')
async def train_data(db: Session = Depends(get_db)):
    train.delay()
    return {'status': 'train success'}


@app.post('/predict')
async def predict_data(predict_text: PredictTextSchema, db: Session = Depends(get_db)):
    result = predict.delay(predict_text.predict_text)
    return {'prediction_result': result.get()}


@app.get('/log')
async def log(db: Session = Depends(get_db)):
    log_file = './trains.log'
    with open(log_file, 'r') as f:
        logs = f.read().split('\n')
    return {'logs': logs}

@app.get('/get_datas')
async def datas_get(db: Session = Depends(get_db)):
    return get_datas(db)


@app.post('/create_data')
async def data_create(data: DataCreateSchema, db: Session = Depends(get_db)):
    return create_data(db, data)


@app.put('/update_data')
async def data_update(data: DataUpdateSchema, inst_id: int, db: Session = Depends(get_db)):
    return update_data(db, data, inst_id)


@app.delete('/delete_data')
async def data_delete(data_id: DataDeleteSchema, db: Session = Depends(get_db)):
    data = get_data(db, data_id.id)
    delete_data(db, data)


@app.post('/upload_file')
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    await save_file(file, db)
    return {"message": f"Successfuly uploaded {file.filename},"}

# if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=8001)