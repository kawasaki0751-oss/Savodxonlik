# Python asosiy tasvirini tanlaymiz
FROM python:3.9-slim

# Ishchi papkani belgilaymiz
WORKDIR /app

# Kutubxonalarni o'rnatish uchun requirements.txt ni ko'chiramiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni ko'chiramiz
COPY . .

# Botni ishga tushiramiz (main.py o'rniga o'z faylingiz nomini yozing)
CMD ["python", "main.py"]