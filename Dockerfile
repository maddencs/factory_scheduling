FROM python:3.13-slim

COPY . .

RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
