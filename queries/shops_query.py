# queries/shops_query.py - Database query functions for Shops and Addresses

from sqlalchemy.orm import Session
from db_models.shops_db_model import Shops, Addresses
from models.shops_model import ShopResponse, ShopWithAddressResponse, AddressResponse


def get_shops_by_user_query(db: Session, user_id: str) -> list[ShopWithAddressResponse]:
    """
    Fetch all shops owned by a specific user, including address details.

    Args:
        db: SQLAlchemy database session
        user_id: The owner's user_id

    Returns:
        List of ShopWithAddressResponse objects
    """
    shops_list = db.query(Shops).filter(Shops.owner_id == user_id).all()
    return [ShopWithAddressResponse.from_orm(shop) for shop in shops_list]


def get_shop_by_id(db: Session, shop_id: str) -> ShopWithAddressResponse | None:
    """
    Fetch a single shop by its shop_id.

    Args:
        db: SQLAlchemy database session
        shop_id: The shop's unique identifier

    Returns:
        ShopWithAddressResponse if found, None otherwise
    """
    shop = db.query(Shops).filter(Shops.shop_id == shop_id).first()
    if shop:
        return ShopWithAddressResponse.from_orm(shop)
    return None


def update_shop_query(db: Session, shop_id: str, shop_data: dict) -> ShopResponse | None:
    """
    Update shop fields by shop_id.

    Args:
        db: SQLAlchemy database session
        shop_id: The shop to update
        shop_data: Dictionary of fields to update

    Returns:
        Updated ShopResponse if successful, None if shop not found
    """
    shop = db.query(Shops).filter(Shops.shop_id == shop_id).first()
    if not shop:
        return None

    for key, value in shop_data.items():
        if hasattr(shop, key) and value is not None:
            setattr(shop, key, value)

    db.commit()
    db.refresh(shop)
    return ShopResponse.from_orm(shop)


def update_address_query(db: Session, address_id: str, address_data: dict) -> AddressResponse | None:
    """
    Update address fields by address_id.

    Args:
        db: SQLAlchemy database session
        address_id: The address to update
        address_data: Dictionary of fields to update

    Returns:
        Updated AddressResponse if successful, None if address not found
    """
    address = db.query(Addresses).filter(Addresses.address_id == address_id).first()
    if not address:
        return None

    for key, value in address_data.items():
        if hasattr(address, key) and value is not None:
            setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return AddressResponse.from_orm(address)