from src.db.database import SessionLocal
from src.db.models import Comment
from src.ai.nlp import get_enbedding

db = SessionLocal()

sample_texts = [
    "گوشی خوبیه ولی باتریش اصلا دوام نداره ",
    "دوربینش فوق العاده هست . برای عکاسی عالی هست",
    "شارژر داخل جعبه نبود که خیلی تو ذوق میزد",
    "صفحه نمایش با کیفیت بالایی دارد"
]

for text in sample_texts:
    vec = get_enbedding(text)
    new_comment = Comment(body = text, rate = 3, enbedding = vec)
    db.add(new_comment)

db.commit()
print("ai sample data injected successfully")