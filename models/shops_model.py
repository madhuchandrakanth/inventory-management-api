# models/shops_model.py - Pydantic models for Shops and Addresses

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---- Address Models ----

class AddressBase(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    country: str


class AddressUpdate(BaseModel):
    """All fields optional for partial updates."""
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class AddressResponse(AddressBase):
    address_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---- Shop Models ----

class ShopBase(BaseModel):
    name: str
    owner_id: str
    address_id: Optional[str] = None


class ShopUpdate(BaseModel):
    """All fields optional for partial updates."""
    name: Optional[str] = None
    owner_id: Optional[str] = None
    address_id: Optional[str] = None


class ShopResponse(ShopBase):
    shop_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShopWithAddressResponse(ShopResponse):
    """Shop response that includes nested address details."""
    address_details: Optional[AddressResponse] = None