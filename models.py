from pydantic import BaseModel
from typing import Optional


# create Address Base Model
class AddressRequest(BaseModel):
    id: Optional[int]
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class GetAddress(BaseModel):
    latitude: float
    longitude: float
    distance: int
