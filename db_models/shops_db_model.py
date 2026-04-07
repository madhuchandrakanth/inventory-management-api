# db_models/shops_db_model.py - SQLAlchemy models for Shops and Addresses tables

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Addresses(Base):
    """Database model for the addresses table."""
    __tablename__ = "addresses"

    address_id = Column(String(255), primary_key=True, unique=True, nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship back to shops
    shops = relationship("Shops", back_populates="address_details")


class Shops(Base):
    """Database model for the shops table."""
    __tablename__ = "shops"

    shop_id = Column(String(255), primary_key=True, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    owner_id = Column(String(255), ForeignKey("users.user_id"), nullable=False)
    address_id = Column(String(255), ForeignKey("addresses.address_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    address_details = relationship("Addresses", back_populates="shops")