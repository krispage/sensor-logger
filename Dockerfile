FROM python:3.9-alpine

RUN adduser -D app

WORKDIR /etc/flask/src/flask_app

RUN apk add --update-cache mysql-client \
        && rm -rf /var/cache/apk/*

RUN apk --update add py3-mysqlclient \
        mariadb-dev \
        build-base

RUN apk add zlib-dev jpeg-dev gcc musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R app:app ./
USER app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

