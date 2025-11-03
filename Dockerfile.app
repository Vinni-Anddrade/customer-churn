FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8085

CMD ["python", "-u", "app.py"]
