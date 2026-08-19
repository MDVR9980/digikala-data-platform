from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ==========================================
# ۱. اسکیماهای کاربر و آدرس (User & Address)
# ==========================================
class AddressBase(BaseModel):
    province: str
    city: str
    postal_code: str
    address_detail: str
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    phone_number: str
    email: Optional[EmailStr] = None
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "customer"

class UserResponse(BaseModel):
    id: int
    phone_number: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True


# ==========================================
# ۲. اسکیماهای برند و دسته‌بندی (Brand & Category)
# ==========================================
class BrandCreate(BaseModel):
    name: str
    slug: str

class BrandResponse(BrandCreate):
    id: int

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    title: str
    slug: str
    parent_id: Optional[int] = None

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# ۳. تنوع کالا و فروشندگان (SellerProduct)
# ==========================================
class SellerProductCreate(BaseModel):
    product_id: int
    seller_name: Optional[str] = "دیجی‌کالا"
    price: int
    discount_percent: Optional[int] = 0
    stock: Optional[int] = 1

class SellerProductResponse(BaseModel):
    id: int
    product_id: int
    seller_name: str
    price: int
    discount_percent: int
    stock: int
    is_active: bool

    class Config:
        from_attributes = True


# ==========================================
# ۴. اسکیماهای نظرات (Comment)
# ==========================================
class CommentCreate(BaseModel):
    product_id: int
    user_id: Optional[int] = None
    title: Optional[str] = None
    body: str
    rate: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    product_id: int
    user_id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    rate: Optional[int] = None
    is_buyer: bool
    sentiment: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# ۵. اسکیماهای محصول (Product)
# ==========================================
class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

class ProductDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    sellers: List[SellerProductResponse] = []
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    id: int
    title: str
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

    class Config:
        from_attributes = True


# ==========================================
# ۶. اسکیماهای سفارشات (Order & OrderItem)
# ==========================================
class OrderItemCreate(BaseModel):
    seller_product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    seller_product_id: int
    quantity: int
    unit_price: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
        