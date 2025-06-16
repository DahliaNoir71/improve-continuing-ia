from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from database import models, schemas
import random
import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility to generate dataset
def generate_dataset(n_samples: int, generation_id: int):
    now = datetime.datetime.now()
    mod_hour = (now.hour % 2) - 0.5
    data = []
    for _ in range(n_samples):
        x1 = random.uniform(-1, 1)
        x2 = random.uniform(-1, 1) * mod_hour
        label = 1 if x1 + x2 > 0 else 0
        data.append(models.DataPoint(
            generation_id=generation_id,
            x1=x1,
            x2=x2,
            label=label
        ))
    return data

@app.post("/generate/")
def generate_data(generation_id: int, n_samples: int = 100, db: Session = Depends(get_db)):
    dataset = generate_dataset(n_samples, generation_id)
    db.add_all(dataset)
    db.commit()
    return {"message": f"Generated {n_samples} samples for generation {generation_id}"}

@app.get("/data/", response_model=list[schemas.DataPointOut])
def get_data(generation_id: int, db: Session = Depends(get_db)):
    return db.query(models.DataPoint).filter(models.DataPoint.generation_id == generation_id).all()
