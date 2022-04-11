from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    name: str = Field(min_length=1)
    street: str = Field(min_length=1)
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)
    latitude: float = Field(gt=-91, lt=91)
    longitude: float = Field(gt=-181, lt=181)
    contact_number: int

ADDRESS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Addressbooks).all()


@app.post("/")
def create_address(address: Address, db: Session = Depends(get_db)):

    address_model = models.Addressbooks()
    address_model.name = address.name
    address_model.street = address.street
    address_model.city = address.city
    address_model.country = address.country
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.contact_number = address.contact_number

    db.add(address_model)
    db.commit()

    return address


@app.put("/{address_id}")
def update_address(address_id: int,address: Address, db: Session = Depends(get_db)):

    address_model = db.query(models.Addressbooks).filter(models.Addressbooks.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Address {address_id}  : Does not exist"
        )

    address_model.name = address.name
    address_model.street = address.street
    address_model.city = address.city
    address_model.country = address.country
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.contact_number = address.contact_number

    db.add(address_model)
    db.commit()

    return address


@app.delete("/{address_id}")
def delete_book(address_id: int, db: Session = Depends(get_db)):
    address_model = db.query(models.Addressbooks).filter(models.Addressbooks.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Address {address_id}  : Does not exist"
        )

    db.query(models.Addressbooks).filter(models.Addressbooks.id == address_id).delete()

    db.commit()


@app.get("/location/{latitude}&{longitude}")
def get_address(latitude: float, longitude: float, db: Session = Depends(get_db)):
    return db.query(models.Addressbooks).filter(models.Addressbooks.latitude == latitude, models.Addressbooks.longitude == longitude).first()


