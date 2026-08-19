from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, 
    Index, Boolean, DateTime, Float
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.database import Base
from pgvector.sqlalchemy import Vector


# --- ۱. مدیریت کاربران ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(String(20), default="customer")  # customer, admin, seller
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship("Comment", back_populates="user")
    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    address_detail = Column(Text, nullable=False)
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")


# --- ۲. دسته‌بندی و برند ---
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    products = relationship("Product", back_populates="category")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), unique=True)

    products = relationship("Product", back_populates="brand")


# --- ۳. محصولات و فروشندگان (Marketplace) ---
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    sellers = relationship("SellerProduct", back_populates="product")
    comments = relationship("Comment", back_populates="product")

    __table_args__ = (
        Index("ix_product_title", "title"),
    )


class SellerProduct(Base):
    __tablename__ = "seller_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_name = Column(String(150), default="دیجی‌کالا")
    price = Column(Integer, nullable=False)
    discount_percent = Column(Integer, default=0)
    stock = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="sellers")


# --- ۴. نظرات و پردازش متن ---
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(300), nullable=True)
    body = Column(Text, nullable=True)
    rate = Column(Integer, nullable=True)
    embedding = Column(Vector(384))
    is_buyer = Column(Boolean, default=False)
    sentiment = Column(String(20), nullable=True)  # positive, negative, neutral
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="comments")
    user = relationship("User", back_populates="comments")


# --- ۵. سفارشات ---
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")  # pending, paid, processing, delivered
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    seller_product_id = Column(Integer, ForeignKey("seller_products.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")