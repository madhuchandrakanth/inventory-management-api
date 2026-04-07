# controller/shops_controller.py - Controller layer for shop endpoints

from sqlalchemy.orm import Session
from services.shops_service import create_shop_service, get_shops_by_user_service, update_shop_service, update_address_service
from models.shops_model import ShopCreate, ShopUpdate, AddressUpdate, ShopResponse, ShopWithAddressResponse, AddressResponse
from typing import List
from fastapi import HTTPException


def handle_create_shop(shop_data: ShopCreate, db: Session) -> ShopResponse:
    """Controller function to create a new shop."""
    result = create_shop_service(db, shop_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


def fetch_shops_by_user(user_id: str, db: Session) -> List[ShopWithAddressResponse]:
    """
    Controller function to fetch all shops for a user.
    """
    return get_shops_by_user_service(db, user_id)


def handle_update_shop(shop_id: str, shop_data: ShopUpdate, db: Session) -> ShopResponse:
    """
    Controller function to update a shop.
    Raises HTTPException if shop not found or no fields provided.
    """
    result = update_shop_service(db, shop_id, shop_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


def handle_update_address(address_id: str, address_data: AddressUpdate, db: Session) -> AddressResponse:
    """
    Controller function to update an address.
    Raises HTTPException if address not found or no fields provided.
    """
    result = update_address_service(db, address_id, address_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
