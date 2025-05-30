from pydantic import BaseModel
from typing import Optional

class IdentifyRequest(BaseModel):
    email: Optional[str]
    phonenumber: Optional[str]

class ContactResponse(BaseModel):
    contact: dict
