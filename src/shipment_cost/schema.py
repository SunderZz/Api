from pydantic import BaseModel

class ShipmentsCostBase(BaseModel):
    Distance: int
    Cost: int