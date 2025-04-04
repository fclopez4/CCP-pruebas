import enum
import uuid

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class IdentificationType(str, enum.Enum):
    CC = "CC"
    CE = "CE"
    NIT = "NIT"


class Manufacturer(Base):
    __tablename__ = "manufacturer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    identification_type = Column(Enum(IdentificationType))
    identification_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    products = relationship(
        "ManufacturerProduct", back_populates="manufacturer"
    )


class ManufacturerProduct(Base):
    __tablename__ = "manufacturer_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manufacturer_id = Column(UUID(as_uuid=True), ForeignKey("manufacturer.id"))
    product_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    manufacturer = relationship("Manufacturer", back_populates="products")
