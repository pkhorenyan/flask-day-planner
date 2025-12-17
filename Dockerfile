FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \

WORKDIR /app

RUN useradd -m -u 1000 flaskuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R flaskuser:flaskuser /app

USER flaskuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
