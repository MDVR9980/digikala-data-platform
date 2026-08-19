from src.db.database import SessionLocal
from src.db.models import Product, Comment


db = SessionLocal()

try:
    # =========================
    # ایجاد 20 محصول
    # =========================

    products = [
        Product(
            title="Samsung Galaxy A55",
            category="موبایل",
            price=18500000
        ),
        Product(
            title="Xiaomi Redmi Note 13",
            category="موبایل",
            price=12500000
        ),
        Product(
            title="Apple iPhone 15",
            category="موبایل",
            price=52000000
        ),
        Product(
            title="Lenovo IdeaPad 3",
            category="لپ تاپ",
            price=32000000
        ),
        Product(
            title="ASUS VivoBook 15",
            category="لپ تاپ",
            price=41000000
        ),
        Product(
            title="MacBook Air M2",
            category="لپ تاپ",
            price=68000000
        ),
        Product(
            title="Sony WH-1000XM5",
            category="هدفون",
            price=18500000
        ),
        Product(
            title="JBL Tune 770NC",
            category="هدفون",
            price=6500000
        ),
        Product(
            title="Logitech G502",
            category="ماوس",
            price=4200000
        ),
        Product(
            title="Redragon K552",
            category="کیبورد",
            price=3800000
        ),
        Product(
            title="LG 24 Inch Monitor",
            category="مانیتور",
            price=9200000
        ),
        Product(
            title="Samsung 27 Inch Monitor",
            category="مانیتور",
            price=14500000
        ),
        Product(
            title="WD External Hard 1TB",
            category="هارد اکسترنال",
            price=4800000
        ),
        Product(
            title="SanDisk Flash 128GB",
            category="فلش مموری",
            price=1100000
        ),
        Product(
            title="Anker PowerBank 20000",
            category="پاوربانک",
            price=3600000
        ),
        Product(
            title="JBL Flip 6",
            category="اسپیکر",
            price=7200000
        ),
        Product(
            title="Xiaomi Smart Watch",
            category="ساعت هوشمند",
            price=5200000
        ),
        Product(
            title="Apple AirPods 3",
            category="هندزفری",
            price=8500000
        ),
        Product(
            title="Canon EOS 2000D",
            category="دوربین",
            price=28000000
        ),
        Product(
            title="Logitech C920",
            category="وبکم",
            price=5600000
        ),
    ]

    db.add_all(products)

    # ذخیره محصولات در PostgreSQL
    db.commit()

    # گرفتن ID واقعی محصولات
    for product in products:
        db.refresh(product)

    print("20 products inserted successfully!")


    # =========================
    # ایجاد کامنت‌ها
    # =========================

    comments = [
        Comment(
            product_id=products[0].id,
            title="گوشی خیلی خوب",
            body="کیفیت ساخت گوشی خیلی خوبه و از خریدش راضی هستم.",
            rate=5
        ),

        Comment(
            product_id=products[0].id,
            title="باتری مناسب",
            body="باتری خوبی داره و برای استفاده روزمره مناسبه.",
            rate=4
        ),

        Comment(
            product_id=products[1].id,
            title="ارزش خرید بالا",
            body="نسبت به قیمتش گوشی مناسبیه.",
            rate=5
        ),

        Comment(
            product_id=products[1].id,
            title="صفحه نمایش خوب",
            body="صفحه نمایش کیفیت خوبی داره.",
            rate=4
        ),

        Comment(
            product_id=products[2].id,
            title="آیفون عالی",
            body="کیفیت دوربین و عملکرد گوشی خیلی خوبه.",
            rate=5
        ),

        Comment(
            product_id=products[3].id,
            title="مناسب برنامه نویسی",
            body="برای کارهای روزمره و برنامه نویسی مناسبه.",
            rate=4
        ),

        Comment(
            product_id=products[4].id,
            title="لپ تاپ خوب",
            body="سرعت مناسبی داره ولی وزنش کمی زیاده.",
            rate=4
        ),

        Comment(
            product_id=products[5].id,
            title="عملکرد عالی",
            body="برای برنامه نویسی و کارهای روزمره عملکرد خیلی خوبی داره.",
            rate=5
        ),

        Comment(
            product_id=products[6].id,
            title="صدای عالی",
            body="صدای بسیار باکیفیتی داره و نویز محیط رو خوب حذف میکنه.",
            rate=5
        ),

        Comment(
            product_id=products[7].id,
            title="هدفون خوب",
            body="نویز کنسلینگش نسبت به قیمت خوبه.",
            rate=4
        ),

        Comment(
            product_id=products[8].id,
            title="مناسب گیمینگ",
            body="برای گیمینگ خیلی خوبه و دقت ماوس بالاست.",
            rate=5
        ),

        Comment(
            product_id=products[9].id,
            title="کیبورد مکانیکال",
            body="کیفیت ساخت مناسبی داره و تایپ کردن باهاش لذت بخشه.",
            rate=4
        ),

        Comment(
            product_id=products[10].id,
            title="مانیتور مناسب",
            body="برای استفاده اداری و برنامه نویسی مناسبه.",
            rate=4
        ),

        Comment(
            product_id=products[11].id,
            title="تصویر عالی",
            body="تصویر واضح و رنگ ها خوب هستند.",
            rate=5
        ),

        Comment(
            product_id=products[12].id,
            title="سرعت مناسب",
            body="سرعت انتقال اطلاعات قابل قبوله.",
            rate=4
        ),

        Comment(
            product_id=products[13].id,
            title="فلش کوچک و سریع",
            body="کوچیک و سبک هست و سرعت مناسبی داره.",
            rate=4
        ),

        Comment(
            product_id=products[14].id,
            title="پاوربانک خوب",
            body="ظرفیت خوبی داره و برای سفر مناسبه.",
            rate=5
        ),

        Comment(
            product_id=products[15].id,
            title="اسپیکر عالی",
            body="صدای اسپیکر خیلی خوب و شفافه.",
            rate=5
        ),

        Comment(
            product_id=products[16].id,
            title="ساعت زیبا",
            body="ظاهر زیبایی داره و امکانات مناسبی ارائه میده.",
            rate=4
        ),

        Comment(
            product_id=products[17].id,
            title="هندزفری با کیفیت",
            body="کیفیت صدا خوبه و اتصال سریعی داره.",
            rate=5
        ),

        Comment(
            product_id=products[18].id,
            title="دوربین مناسب",
            body="برای عکاسی مبتدی گزینه مناسبیه.",
            rate=4
        ),

        Comment(
            product_id=products[19].id,
            title="وبکم خوب",
            body="کیفیت تصویر برای جلسات آنلاین خیلی خوبه.",
            rate=5
        ),
    ]

    db.add_all(comments)

    # ذخیره کامنت‌ها
    db.commit()

    print("22 comments inserted successfully!")
    print("Seed completed successfully!")


except Exception as e:
    db.rollback()
    print("Error:", e)


finally:
    db.close()