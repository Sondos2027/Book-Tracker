from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Book
from database import get_db, BookDB

app = FastAPI()

# 1. رابط الصفحة الرئيسية
@app.get("/")
def home():
    return {"message": "مرحباً بك في نظام إدارة الكتب الاحترافي!"}

# 2. رابط عرض كل الكتب من قاعدة البيانات
@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(BookDB).all()
    return books

# 3. رابط إضافة كتاب جديد وحفظه في الملف
@app.post("/books")
def create_book(book: Book, db: Session = Depends(get_db)):
    # التأكد من أن الـ ID غير مكرر في قاعدة البيانات
    db_book = db.query(BookDB).filter(BookDB.id == book.id).first()
    if db_book:
        raise HTTPException(status_code=400, detail="هذا الرقم التعريفي (ID) موجود مسبقاً")
    
    # تحويل بيانات الكتاب وحفظها
    new_book = BookDB(id=book.id, title=book.title, author=book.author, year=book.year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "تم حفظ الكتاب بنجاح في قاعدة البيانات!", "book": new_book}
