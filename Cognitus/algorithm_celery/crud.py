from sqlalchemy.orm import Session
from models import DataModel, LogModel
import pandas as pd
from database import engine


def get_datas(db: Session):
    return db.query(DataModel).all()


def get_data(db: Session, data_id: int):
    return db.query(DataModel).filter(DataModel.id == data_id).first()


def create_data(db: Session, data: DataModel):
    data = DataModel(**data.model_dump())
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except Exception as e :
        raise ValueError('Error creating new data')


def update_data(db: Session, data: DataModel, inst_id: int):
    existing_data = db.query(DataModel).filter(DataModel.id == inst_id).first()  # !!

    if not data:
        return [{"error": "error"}]
    
    instance = DataModel(**data.model_dump())

    if instance:
        try:
            existing_data.text = instance.text
            existing_data.label = instance.label
            db.commit()
            db.refresh(existing_data)
        except Exception as e :
            raise ValueError('Error updating data')
    return data


def delete_data(db: Session, data: DataModel):
    try:
        db.delete(data)
        db.commit()
        return [{"post_deleted": True}]
    except Exception as e:
        raise ValueError('Error deleting data')

async def save_file(file, db: Session):
    with open(file.filename, 'wb') as f:
        f.write(await file.read())

    df = pd.read_excel(file.filename)
    text, label = df['text'], df['label']

    for i in range(len(text)):
        data = {
            'text': text[i],
            'label': label[i]
        }
        d = DataModel(**data)
        db.add(d)
        db.commit()
        db.refresh(d)

    return {'status': 'success'}


# Log

def addLog(log: LogModel, db: Session):
    log_ = LogModel(**log.model_dump())
    try:
        db.add(log_)
        db.commit()
        db.refresh(log_)
        return log

    except Exception as e :
        raise ValueError(f'Error creating new log: {e}')

def getLog(db: Session):
    return db.query(LogModel).all()
