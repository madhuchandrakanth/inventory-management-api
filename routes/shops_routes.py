# routes/shops_routes.py - API routes for shop endpoints

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controller.shops_controller import handle_create_shop, fetch_shops_by_user, handle_update_shop, handle_update_address
from models.shops_model import ShopCreate, ShopUpdate, AddressUpdate
from database import get_db

# Create a dedicated router for Shops
shop_router = APIRouter(prefix="/shops", tags=["Shops"])


@shop_router.post("/")
def create_shop(shop_data: ShopCreate, db: Session = Depends(get_db)):
    """POST /shops - Create a new shop"""
    return handle_create_shop(shop_data, db)


@shop_router.get("/{user_id}")
def get_shops_by_user(user_id: str, db: Session = Depends(get_db)):
    """GET /shops/{user_id} - Fetch all shops owned by a user"""
    return fetch_shops_by_user(user_id, db)


@shop_router.put("/{shop_id}")
def update_shop(shop_id: str, shop_data: ShopUpdate, db: Session = Depends(get_db)):
    """
    PUT /shops/{shop_id} - Update a shop's details
    """
    return handle_update_shop(shop_id, shop_data, db)


@shop_router.put("/address/{address_id}")
def update_address(address_id: str, address_data: AddressUpdate, db: Session = Depends(get_db)):
    """
    PUT /shops/address/{address_id} - Update an address
    """
    return handle_update_address(address_id, address_data, db)
