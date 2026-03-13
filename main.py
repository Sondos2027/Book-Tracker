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

# 3. رابط إضافة كتاب جديد (POST) 
@app.post("/books")
def create_book(book: Book):
    # التحقق من أن الرقم التعريفي (ID) غير مكرر - Error Handling 
    for existing_book in db_books:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=400, detail="هذا الرقم التعريفي (ID) موجود مسبقاً، يرجى استخدام رقم آخر.")
    
    # تحويل البيانات القادمة من المتدرب/المستخدم إلى قاموس (Dictionary)g 
    new_book_data = book.dict()
    
    # إضافة الكتاب للقائمة (قاعدة البيانات الوهمية)
    db_books.append(new_book_data)
    
    return {"message": "تم إضافة الكتاب بنجاح!", "book": new_book_data}