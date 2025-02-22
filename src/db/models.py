from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    telegram_user_id = Column(BigInteger, primary_key=True)
    balance = Column(Numeric(10, 2), default=0)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Proxy(Base):
    __tablename__ = "proxies"
    id = Column(Integer, primary_key=True)
    ip = Column(String(45), nullable=False)  
    port = Column(Integer, nullable=False)
    protocol = Column(String(20), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_assigned = Column(Boolean, default=False) 


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_user_id", ondelete="CASCADE"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Numeric(10, 2), nullable=False)   

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    proxy_id = Column(Integer, ForeignKey("proxies.id", ondelete="RESTRICT"), nullable=False)
    valid_until = Column(DateTime, nullable=False)

    order = relationship("Order", back_populates="order_items")
    proxy = relationship("Proxy")

