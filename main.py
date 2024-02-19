from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, Integer, Float, Numeric, create_engine
import datetime
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.environ["DB_PATH"]
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

Base.metadata.create_all(engine)

class Stat(Base):
    __tablename__ = 'stat'
    id = Column(Integer, primary_key=True, index=True)
    device = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(Numeric)

class Result(BaseModel):
    x: float
    y: float
    z: float

@app.get('/devices/{device}/stats')
def get_stat(device: int, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    return resp

@app.get('/devices/{device}/stats/{val}/median')
def get_median(device: int, val: str, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    vals = [i.__dict__[val] for i in resp]
    return np.median(vals)

@app.get('/devices/{device}/stats/{val}/sum')
def get_median(device: int, val: str, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    vals = [i.__dict__[val] for i in resp]
    return np.sum(vals)

@app.get('/devices/{device}/stats/{val}/amount')
def get_median(device: int, val: str, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    vals = [i.__dict__[val] for i in resp]
    return len(vals)

@app.get('/devices/{device}/stats/{val}/max')
def get_median(device: int, val: str, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    vals = [i.__dict__[val] for i in resp]
    return np.max(vals)

@app.get('/devices/{device}/stats/{val}/min')
def get_median(device: int, val: str, db: Session = Depends(get_db)):
    resp = db.query(Stat).filter(Stat.device == device).all()
    vals = [i.__dict__[val] for i in resp]
    return np.min(vals)

@app.get('/devices/stats')
def get_stat(db: Session = Depends(get_db)):
    resp = db.query(Stat).all()
    return resp

@app.post('/devices/{device}/stats')
def create_user(device: int, request: Result, db: Session = Depends(get_db)):
    new_stat = Stat(device = device, x = request.x, y = request.y, z = request.z, timestamp = int(datetime.datetime.now().timestamp()))
    db.add(new_stat)
    db.commit()
    db.refresh(new_stat)
    return new_stat


