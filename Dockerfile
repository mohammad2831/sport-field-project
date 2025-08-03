FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sport.wsgi:application"]

