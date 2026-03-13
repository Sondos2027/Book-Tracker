from fastapi import FastAPI, HTTPException
from models import Book
from database import db_books  # استيراد القائمة من ملفها الجديد

app = FastAPI()

# 1. رابط الصفحة الرئيسية (GET)
@app.get("/")
def home():
    return {"message": "مرحباً بك في نظام إدارة الكتب!"}

# 2. رابط عرض كل الكتب (GET) 
@app.get("/books")
def get_all_books():
    return db_books # إرجاع البيانات بصيغة JSON تلقائياً
