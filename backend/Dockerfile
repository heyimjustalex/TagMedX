
FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update
RUN apt-get install -y pkg-config
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
