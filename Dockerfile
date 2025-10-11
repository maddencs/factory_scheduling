FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
