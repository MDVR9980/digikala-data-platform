from src.db.database import engine, Base
# ایمپورت تمام مدل‌ها برای اینکه SQLAlchemy جداول را شناسایی کند
import src.db.models 

def create_database_tables():
    print("⏳ در حال ساخت جداول دیتابیس...")
    Base.metadata.create_all(bind=engine)
    print("✅ تمامی جداول با موفقیت ساخته شدند.")

if __name__ == "__main__":
    create_database_tables()
    