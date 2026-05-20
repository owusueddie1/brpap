from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    business_data = relationship("BusinessData", back_populates="owner")


class BusinessData(Base):
    __tablename__ = "business_data"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    upload_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=True)

    owner = relationship("User", back_populates="business_data")
