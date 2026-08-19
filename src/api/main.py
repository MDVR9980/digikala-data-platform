from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, desc
import pandas as pd
import io
import os
from pathlib import Path

# ایمپورت‌های پروژه
from src.ai.nlp import get_enbedding
from src.db.database import get_db, engine
from src.db.models import (
    User, Address, Category, Brand, 
    Product, SellerProduct, Comment, Order, OrderItem
)
from src.api.schemas import (
    UserCreate, UserResponse,
    AddressCreate, AddressResponse,
    CategoryCreate, CategoryResponse,
    BrandCreate, BrandResponse,
    ProductCreate, ProductListResponse, ProductDetailResponse,
    SellerProductCreate, SellerProductResponse,
    CommentCreate, CommentResponse,
    OrderCreate, OrderResponse
)

app = FastAPI(
    title="Digikala Complete API Platform",
    description="سیستم جامع سرویس‌های دیجی‌کالا برای تمامی مدل‌ها",
    version="2.0.0"
)

# =========================================================
# ⚙️ تنظیمات مسیرهای استاتیک و قالب‌ها (HTML)
# =========================================================
# پیدا کردن مسیر اصلی پروژه (Root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# متصل کردن پوشه static (واقع در روت پروژه)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# تنظیمات Jinja2 برای پیدا کردن پوشه templates (واقع در روت پروژه)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# =========================================================
# 🖥️ روت‌های فرانت‌اند (UI - رندر صفحات HTML بصورت SSR)
# =========================================================
@app.get("/", tags=["UI"])
def render_home(request: Request, db: Session = Depends(get_db)):
    # دریافت داینامیک دیتا از دیتابیس برای نمایش در صفحه اصلی
    products = db.query(Product).limit(15).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="pages/index.html", 
        context={"products": products}
    )

@app.get("/product/{product_id}", tags=["UI"])
def render_product_page(request: Request, product_id: int, db: Session = Depends(get_db)):
    # دریافت کامل اطلاعات محصول، فروشندگان و نظرات از دیتابیس
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="محصول یافت نشد")
        
    sellers = db.query(SellerProduct).filter(SellerProduct.product_id == product_id).all()
    comments = db.query(Comment).filter(Comment.product_id == product_id).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="pages/product.html", 
        context={
            "product": product,
            "sellers": sellers,
            "comments": comments
        }
    )


# =========================================================
# 👤 ۱. کاربران (Users)
# =========================================================
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone_number == user_in.phone_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="شماره تماس قبلاً ثبت شده است.")
    
    user = User(
        phone_number=user_in.phone_number,
        email=user_in.email,
        hashed_password=user_in.password,  # در حالت عملیاتی با bcrypt هش شود
        full_name=user_in.full_name,
        role=user_in.role or "customer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد.")
    return user

@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_all_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


# =========================================================
# 📍 ۲. آدرس‌ها (Addresses)
# =========================================================
@app.post("/users/{user_id}/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED, tags=["Addresses"])
def add_address_for_user(user_id: int, address_in: AddressCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر مورد نظر یافت نشد.")
    
    address = Address(
        user_id=user_id,
        province=address_in.province,
        city=address_in.city,
        postal_code=address_in.postal_code,
        address_detail=address_in.address_detail,
        is_default=address_in.is_default
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

@app.get("/users/{user_id}/addresses", response_model=List[AddressResponse], tags=["Addresses"])
def get_user_addresses(user_id: int, db: Session = Depends(get_db)):
    return db.query(Address).filter(Address.user_id == user_id).all()


# =========================================================
# 🏷️ ۳. برندها و دسته‌بندی‌ها (Brands & Categories)
# =========================================================
@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_category(cat_in: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**cat_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@app.get("/categories", response_model=List[CategoryResponse], tags=["Categories"])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@app.post("/brands", response_model=BrandResponse, status_code=status.HTTP_201_CREATED, tags=["Brands"])
def create_brand(brand_in: BrandCreate, db: Session = Depends(get_db)):
    brand = Brand(**brand_in.model_dump())
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

@app.get("/brands", response_model=List[BrandResponse], tags=["Brands"])
def get_all_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()


# =========================================================
# 📦 ۴. محصولات (Products)
# =========================================================
@app.post("/products", response_model=ProductListResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products", response_model=List[ProductListResponse], tags=["Products"])
def get_all_products(
    skip: int = 0, 
    limit: int = 10,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if brand_id:
        query = query.filter(Product.brand_id == brand_id)
    return query.offset(skip).limit(limit).all()

@app.get("/products/search", response_model=List[ProductListResponse], tags=["Products"])
def search_products(q: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.title.contains(q)).all()

@app.get("/products/{product_id}", response_model=ProductDetailResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="کالا پیدا نشد.")
    return product


# =========================================================
# 🏪 ۵. تنوع فروشندگان و قیمت (Seller Products)
# =========================================================
@app.post("/seller-products", response_model=SellerProductResponse, status_code=status.HTTP_201_CREATED, tags=["Seller Products"])
def add_seller_to_product(item_in: SellerProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="محصول مورد نظر وجود ندارد.")

    seller_item = SellerProduct(**item_in.model_dump())
    db.add(seller_item)
    db.commit()
    db.refresh(seller_item)
    return seller_item

@app.get("/products/{product_id}/sellers", response_model=List[SellerProductResponse], tags=["Seller Products"])
def get_sellers_for_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(SellerProduct).filter(SellerProduct.product_id == product_id).all()


# =========================================================
# 💬 ۶. نظرات (Comments)
# =========================================================
@app.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, tags=["Comments"])
def add_comment(comment_in: CommentCreate, db: Session = Depends(get_db)):
    comment = Comment(**comment_in.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@app.get("/products/{product_id}/comments", response_model=List[CommentResponse], tags=["Comments"])
def get_product_comments(product_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.product_id == product_id).all()

@app.get("/products/{product_id}/comments/top", response_model=List[CommentResponse], tags=["Comments"])
def get_top_comments(product_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.product_id == product_id, Comment.rate >= 4).all()


# =========================================================
# 🛒 ۷. سفارشات (Orders & Order Items)
# =========================================================
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    # بررسی وجود کاربر
    user = db.query(User).filter(User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد.")

    total_price = 0
    order_items_to_create = []

    # محاسبه قیمت کل و چک کردن موجودی
    for item in order_in.items:
        seller_item = db.query(SellerProduct).filter(SellerProduct.id == item.seller_product_id).first()
        if not seller_item or seller_item.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"موجودی کالا با شناسه تنوع {item.seller_product_id} کافی نیست."
            )
        
        # اعمال تخفیف در صورت وجود
        unit_price = seller_item.price * (100 - seller_item.discount_percent) // 100
        total_price += unit_price * item.quantity
        
        # کسر از انبار
        seller_item.stock -= item.quantity

        order_items_to_create.append(
            OrderItem(
                seller_product_id=item.seller_product_id,
                quantity=item.quantity,
                unit_price=unit_price
            )
        )

    # ثبت سفارش
    new_order = Order(
        user_id=order_in.user_id,
        total_price=total_price,
        status="pending",
        items=order_items_to_create
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="سفارش یافت نشد.")
    return order

@app.get("/users/{user_id}/orders", response_model=List[OrderResponse], tags=["Orders"])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).all()


# =========================================================
# 📊 ۸. آمار و تحلیل داده (Analytics)
# =========================================================
@app.get("/analytics/top-products", tags=["Analytics"])
def get_top_products(db: Session = Depends(get_db)):
    results = db.query(
        Comment.product_id,
        func.count(Comment.id).label("total_comments"),
        func.avg(Comment.rate).label("average_rate")
    ).group_by(Comment.product_id).order_by(desc("total_comments")).limit(5).all()

    report = []
    for row in results:
        report.append({
            "product_id": row.product_id,
            "total_comments": row.total_comments,
            "average_rate": round(row.average_rate, 2) if row.average_rate else None
        })
    return report

@app.get("/analytics/export_report", tags=["Analytics"])
def export_analytics_csv(db: Session = Depends(get_db)):
    query = db.query(Comment.product_id, Comment.rate).statement
    df = pd.read_sql(query, engine)

    report_df = df.groupby("product_id").agg(
        total_comments=("product_id", "count"),
        average_rate=("rate", "mean")
    ).reset_index()

    stream = io.StringIO()
    report_df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=digikala_analytics_report.csv"
    return response

@app.get("/search/comments")
def semantic_search_comments(query:str,limit:int=5,db: Session = Depends(get_db)):
    query_vector = get_enbedding(query)
    similar_comments = db.query(Comment).filter(Comment.embedding.is_not(None)).order_by(Comment.embedding.cosine_distance(query_vector)).limit(limit).all()

    results = []
    for comment in similar_comments:
        results.append({
            "id": comment.id,
            "body": comment.body,
            "rate": comment.rate
        })
    return results