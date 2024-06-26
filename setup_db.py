from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(String, primary_key=True)
    flight_number = Column(String)
    airline = Column(String)
    origin = Column(String)
    destination = Column(String)
    scheduled_departure_at = Column(DateTime)
    actual_departure_at = Column(DateTime)
    scheduled_arrival_at = Column(DateTime)
    actual_arrival_at = Column(DateTime)

class Delay(Base):
    __tablename__ = 'delays'
    id = Column(String, primary_key=True)
    flight_number = Column(String)
    delay_code = Column(String)
    delay_time = Column(Integer)
    description = Column(String)

# Database setup
engine = create_engine('sqlite:///flights.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
