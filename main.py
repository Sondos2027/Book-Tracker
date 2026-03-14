
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Book as BookSchema, BookCreate  # استيراد الموديلات الجديدة
from database import get_db, BookDB                # استيراد إعدادات قاعدة البيانات

app = FastAPI()

# 1. رابط الصفحة الرئيسية
@app.get("/")
def home():
    return {"message": "مرحباً بك في نظام إدارة الكتب الاحترافي!"}

# 2. رابط عرض كل الكتب من قاعدة البيانات
@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    # جلب كل السجلات من جدول الكتب
    books = db.query(BookDB).all()
    return books

# 3. رابط إضافة كتاب جديد (بدون الحاجة لإدخال ID يدوياً)
@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # بما أننا نستخدم autoincrement، لا نحتاج للتأكد من الـ ID يدوياً
    # نقوم بإنشاء كائن جديد من BookDB وحفظ البيانات فيه
    new_book = BookDB(
        title=book.title, 
        author=book.author, 
        year=book.year
    )
    
    try:
        db.add(new_book)      # إضافة الكتاب للجلسة
        db.commit()           # حفظ التغييرات نهائياً في ملف books.db
        db.refresh(new_book)  # استرجاع البيانات المحدثة (بما فيها الـ ID الذي وُلد تلقائياً)
        return {"message": "تم حفظ الكتاب بنجاح!", "book": new_book}
    except Exception as e:
        db.rollback()         # في حال حدوث خطأ، يتم التراجع عن المحاولة
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء الحفظ في قاعدة البيانات")

# 4. رابط لجلب كتاب محدد بواسطة الـ ID               
@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="عذراً، الكتاب غير موجود")
    return book


# 5. رابط تحديث بيانات كتاب (PUT)
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book_query = db.query(BookDB).filter(BookDB.id == book_id)
    existing_book = book_query.first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="الكتاب غير موجود لتحديثه")
    try:
        book_query.update({
            "title": updated_book.title,
            "author": updated_book.author,
            "year": updated_book.year
        }, synchronize_session=False)
        db.commit()
        return {"message": "تم التحديث بنجاح!", "book": updated_book}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="خطأ في التحديث")


# 6. رابط حذف كتاب نهائياً (DELETE)
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="الكتاب غير موجود لحذفه")
    try:
        db.delete(book)
        db.commit()
        return {"message": f"تم حذف الكتاب رقم {book_id} بنجاح!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="خطأ في الحذف")