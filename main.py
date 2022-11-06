from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from pydantic import fields
from random import randrange
import uvicorn
from database import Base, engine, Address, get_session
from models import AddressRequest, GetAddress
from sqlalchemy.orm import Session
from geopy.geocoders import Nominatim

# create the database
Base.metadata.create_all(engine)

# initialize the app
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload = True)

@app.post("/create_address", status_code=status.HTTP_201_CREATED)
def create_address(new_address:AddressRequest, session: Session = Depends(get_session)):
    

    # get latitude and longitude from address
    location = Nominatim(user_agent="GetLoc")
    getLoc = location.geocode(new_address.address)
    print(getLoc.address)

    # create an instance of Address db model
    addressdb = Address(id = new_address.id,
    address = new_address.address,    
    latitude = getLoc.latitude,
    longitude = getLoc.longitude)

    # add it to the session and commit it
    session.add(addressdb)
    session.commit()
    
    # refresh db 
    session.refresh(addressdb)
    
    # grab the id given to object from db
    id = addressdb.id

    return f'created address with id = {id} '

@app.get("/get_address/{id}")
async def get_address(id:int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(Address).get(id)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(status_code=404, detail=f"address with id {id} not found")

    return address

@app.delete("/delete_address/{id}")
def address_delete(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(Address).get(id)

    # if address item with given id exists, delete it from the database. Otherwise raise 404 error
    if address:
        session.delete(address)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Address with id {id} not found")

    return None



@app.put("/update_address/{id}")
def update_address(id: int, address: str, session: Session = Depends(get_session)):

    instance = session.query(Address).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if instance:
        instance.address = address
        
        session.commit()


    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not instance:
        raise HTTPException(status_code=404, detail=f"address item with id {id} not found")

    return instance


@app.get("/get_address_list", status_code=status.HTTP_200_OK)
def get_address_list(session: Session = Depends(get_session)):

    # get all addresses
    address_list = session.query(Address).all()

    return address_list