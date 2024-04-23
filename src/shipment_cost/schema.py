from pydantic import BaseModel

class ShipmentsCostBase(BaseModel):
    distance: int
    cost: int