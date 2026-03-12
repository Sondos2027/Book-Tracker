from fastapi import FastAPI
from models import Book

app = FastAPI()

# قاعدة بيانات وهمية (قائمة بسيطة) لتخزين الكتب مؤقتاً
db_books = [
    {"id": 1, "title": "Clean Code", "author": "Robert Martin", "year": 2008}
]

@app.get("/")
def home():
    return {"message": "مرحباً بك في نظام إدارة الكتب!"}

@app.get("/books")
def get_all_books():
    return db_books # إرجاع البيانات بصيغة JSON تلقائياً

