FROM python:3.12-alpine3.21

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]