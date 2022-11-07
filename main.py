import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session

from database import Base, engine, Address, get_session
from models import AddressRequest, GetAddress

# create the database
Base.metadata.create_all(engine)

# initialize the app
app = FastAPI()

# Run Server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)


# Create Address
@app.post("/create_address", status_code=status.HTTP_201_CREATED)
def create_address(new_address: AddressRequest, session: Session = Depends(get_session)):
    """
    For creating address we required only address and id.
    """
    # get latitude and longitude from address
    location = Nominatim(user_agent="GetLoc")
    getLoc = location.geocode(new_address.address)
    print(getLoc.address)

    # create an instance of Address db model
    addressdb = Address(id=new_address.id,
                        address=new_address.address,
                        latitude=getLoc.latitude,
                        longitude=getLoc.longitude)

    # add it to the session and commit it
    session.add(addressdb)
    session.commit()
    session.refresh(addressdb)

    # grab the id given to object from db
    id = addressdb.id

    return f'created address with id = {id} '


# Retrieve Address
@app.get("/get_address/{id}")
async def get_address(id: int, session: Session = Depends(get_session)):
    """
    Only required id of given address.
    """
    # get the address item with the given id
    address = session.query(Address).get(id)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(
            status_code=404, detail=f"address with id {id} not found")

    return address


# Update Address
@app.put("/update_address/{id}")
def update_address(id: int, new_address: AddressRequest, session: Session = Depends(get_session)):
    """
        For updating address only address field is required.
    """
    instance = session.query(Address).get(id)

    # get latitude and longitude from address
    location = Nominatim(user_agent="GetLoc")
    getLoc = location.geocode(new_address.address)

    # update address item with the given address (if an address with the given id was found)
    if instance:
        instance.address = new_address.address
        instance.latitude = getLoc.latitude
        instance.longitude = getLoc.longitude
        session.add(instance)
        session.commit()

    # check if address with given id exists. If not, raise exception and return 404 not found response
    if not instance:
        raise HTTPException(
            status_code=404, detail=f"address item with id {id} not found")

    return instance


# Delete Address
@app.delete("/delete_address/{id}")
def address_delete(id: int, session: Session = Depends(get_session)):
    """
    Deleting address we required only id.
    """
    # get the address item with the given id
    address = session.query(Address).get(id)

    # if address item with given id exists, delete it from the database. Otherwise raise 404 error
    if address:
        session.delete(address)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"Address with id {id} not found")

    return None


# Get All Address
@app.post("/get_address_list", status_code=status.HTTP_200_OK)
def get_address_list(address: GetAddress, session: Session = Depends(get_session)):
    """
    Distance must be in kilometers.
    """
    location_1 = (address.latitude, address.longitude)
    distance = address.distance

    data = session.query(Address).all()

    myAddress = []

    for i in data:
        location_2 = (i.latitude, i.longitude)
        cal_distance = geodesic(location_1, location_2).km
        if cal_distance <= distance:
            myAddress.append(f'Address = {i.address} with id = {i.id} ')

    return myAddress
