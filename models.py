from sqlalchemy import Column, Integer, String, Float
from database import Base


class Addressbooks(Base):
    __tablename__ = "addressbook"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    street = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    contact_number = Column(Integer)
