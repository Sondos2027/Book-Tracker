# 1. القاعدة (Base Image)
FROM python:3.12-slim

# 2. مجلد العمل (Working Directory)
WORKDIR /app

# 3. تجهيز المكتبات (Dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. نقل الكود (Copy Source Code)
COPY . .

# 5. المنفذ (Port)
EXPOSE 8080

# 6. التشغيل (Command)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]