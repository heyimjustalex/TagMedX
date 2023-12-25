FROM python:3.12.1-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apk --no-cache add build-base=0.5-r3 py3-pkgconfig=1.5.5-r3 mariadb-dev=10.11.5-r3 \
    && pip install --no-cache-dir --upgrade pip==23.3.2 \
    && pip install --no-cache-dir -r requirements.txt \
    && mkdir /images \
    && adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser /app /images

USER appuser

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
