from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base
from typing import Optional

# 1. كلاس SQLAlchemy (لوصف الجدول في قاعدة البيانات)
class Book(Base):
    __tablename__ = "books"
    # هذا هو السطر المنقذ
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
  # 2. كلاس Pydantic (لوصف البيانات القادمة من المستخدم عبر الـ API)
class BookCreate(BaseModel):
    # هنا جعلنا الـ id اختيارياً أو حذفناه تماماً من المدخلات
    # لكي لا يظهر خطأ 422 إذا لم يرسله المستخدم
    title: str
    author: str
    year: int

    class Config:
        from_attributes = True    
