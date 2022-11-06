from pydantic import BaseModel
from typing import Optional

# create Address Base Model
class AddressRequest(BaseModel):
    id : Optional[int]
    address : str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class GetAddress(BaseModel):
    latitude_1: float
    longitude_1: float
    latitude_2: float  
    longitude_2: float   