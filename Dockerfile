# 1. اختيار نظام التشغيل ولغة البرمجة
FROM python:3.12-slim

# 2. إضافة المتغيرات البيئية 
# APP_ENV يحدد أن التطبيق يعمل في وضع الإنتاج
ENV APP_ENV=production
# تمنع بايثون من إنشاء ملفات pyc مؤقتة
ENV PYTHONDONTWRITEBYTECODE 1
# تضمن ظهور رسائل الـ Logs فوراً في Terminal دوكر
ENV PYTHONUNBUFFERED 1

# 3. تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# 4. نسخ ملف المكتبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ كود المشروع بالكامل
COPY . .

# 6. أمر تشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

