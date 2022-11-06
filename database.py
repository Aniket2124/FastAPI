from sqlalchemy import create_engine, Column, Integer, String, Float 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create a sqlite engine instance
engine = create_engine("sqlite:///address.db")

# Create SessionLocal class from sessionmaker factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# create a declarativeMeta instance
Base = declarative_base()

# define address class inheriting from Base
class Address(Base):
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True)
    address = Column(String(255))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()