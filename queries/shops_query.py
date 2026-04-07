# queries/shops_query.py - Database query functions for Shops and Addresses

import uuid

from sqlalchemy.orm import Session
from db_models.shops_db_model import Shops, Addresses
from models.shops_model import ShopCreate, ShopResponse, ShopWithAddressResponse, AddressResponse


def get_shop_by_name_and_owner(db: Session, name: str, owner_id: str) -> Shops | None:
    """Check if a shop with the same name already exists for this owner."""
    return db.query(Shops).filter(
        Shops.name == name,
        Shops.owner_id == owner_id
    ).first()


def create_shop_query(db: Session, shop_data: ShopCreate) -> ShopWithAddressResponse | None:
    """Create a new address + shop in the database. Returns None if FK constraint fails."""
    from sqlalchemy.exc import IntegrityError

    address_id = None

    # Create address record if any address fields are provided
    if any([shop_data.address, shop_data.city, shop_data.state, shop_data.pincode]):
        address_id = str(uuid.uuid4())
        db_address = Addresses(
            address_id=address_id,
            address=shop_data.address or "",
            city=shop_data.city or "",
            state=shop_data.state or "",
            zip_code=shop_data.pincode or "",
            country="India",
        )
        db.add(db_address)

    db_shop = Shops(
        shop_id=str(uuid.uuid4()),
        name=shop_data.name,
        owner_id=shop_data.owner_id,
        address_id=address_id,
    )
    try:
        db.add(db_shop)
        db.commit()
        db.refresh(db_shop)
        return ShopWithAddressResponse.from_orm(db_shop)
    except IntegrityError:
        db.rollback()
        return None


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


def update_shop_query(db: Session, shop_id: str, shop_data: dict) -> ShopWithAddressResponse | None:
    """
    Update shop and its address by shop_id.
    If address fields are provided and no address exists, creates a new one.
    """
    shop = db.query(Shops).filter(Shops.shop_id == shop_id).first()
    if not shop:
        return None

    # Separate address fields from shop fields
    address_field_map = {
        "address": "address",
        "city": "city",
        "state": "state",
        "pincode": "zip_code",
    }
    # Fields that belong to address, not shop
    non_shop_fields = {"address", "city", "state", "pincode", "district", "type"}

    address_updates = {}
    for frontend_key, db_key in address_field_map.items():
        if frontend_key in shop_data and shop_data[frontend_key] is not None:
            address_updates[db_key] = shop_data[frontend_key]

    # Update or create address if address fields provided
    if address_updates:
        if shop.address_id:
            # Update existing address
            existing_address = db.query(Addresses).filter(Addresses.address_id == shop.address_id).first()
            if existing_address:
                for key, value in address_updates.items():
                    setattr(existing_address, key, value)
        else:
            # Create new address and link it
            new_address_id = str(uuid.uuid4())
            db_address = Addresses(
                address_id=new_address_id,
                address=address_updates.get("address", ""),
                city=address_updates.get("city", ""),
                state=address_updates.get("state", ""),
                zip_code=address_updates.get("zip_code", ""),
                country="India",
            )
            db.add(db_address)
            shop.address_id = new_address_id

    # Update shop fields (only columns that exist on the Shops model)
    for key, value in shop_data.items():
        if key not in non_shop_fields and hasattr(shop, key) and value is not None:
            setattr(shop, key, value)

    db.commit()
    db.refresh(shop)
    return ShopWithAddressResponse.from_orm(shop)


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