from pydantic import BaseModel

class Shop:
    shop_id: str
    name: str
    owner_id: str
    address_id: str
    created_at: str
    updated_at: str

class Address:
    address_id: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    created_at: str
    updated_at: str