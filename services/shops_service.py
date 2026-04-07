# services/shops_service.py - Business logic layer for shop operations

from sqlalchemy.orm import Session
from queries.shops_query import (
    get_shops_by_user_query,
    get_shop_by_id,
    get_shop_by_name_and_owner,
    create_shop_query,
    update_shop_query,
    update_address_query,
)
from models.shops_model import ShopCreate, ShopUpdate, AddressUpdate, ShopResponse, ShopWithAddressResponse, AddressResponse


def create_shop_service(db: Session, shop_data: ShopCreate) -> ShopResponse | dict:
    """Creates a new shop. Returns error if shop with same name already exists for this owner."""
    existing = get_shop_by_name_and_owner(db, shop_data.name, shop_data.owner_id)
    if existing:
        return {"error": "Shop with this name already exists"}
    result = create_shop_query(db, shop_data)
    if not result:
        return {"error": "Invalid owner_id - user does not exist"}
    return result


def get_shops_by_user_service(db: Session, user_id: str) -> list[ShopWithAddressResponse]:
    """
    Service function to get all shops for a user.
    Add authorization or filtering logic here as needed.
    """
    return get_shops_by_user_query(db, user_id)


def update_shop_service(db: Session, shop_id: str, shop_data: ShopUpdate) -> ShopResponse | dict:
    """
    Service function to update a shop.
    Validates the shop exists and applies partial updates.
    """
    # Convert to dict, excluding unset fields
    update_dict = shop_data.model_dump(exclude_unset=True)

    if not update_dict:
        return {"error": "No fields provided for update"}

    result = update_shop_query(db, shop_id, update_dict)
    if not result:
        return {"error": "Shop not found"}
    return result


def update_address_service(db: Session, address_id: str, address_data: AddressUpdate) -> AddressResponse | dict:
    """
    Service function to update an address.
    Validates the address exists and applies partial updates.
    """
    update_dict = address_data.model_dump(exclude_unset=True)

    if not update_dict:
        return {"error": "No fields provided for update"}

    result = update_address_query(db, address_id, update_dict)
    if not result:
        return {"error": "Address not found"}
    return result
