FROM python:3.12-alpine
LABEL authors="laredo"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# Comando temporário para debugar:
RUN ls -la /app

CMD ["python", "main.py"]
