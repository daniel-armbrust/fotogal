#
# Dockerfile
#
FROM python:3.8-alpine

LABEL maintainer="Daniel Armbrust <darmbrust@gmail.com>"

ENV FLASK_APP=fotogal.py
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production
ENV STATIC_URL=/static
ENV STATIC_PATH=/opt/fotogal/app/static

WORKDIR /opt/fotogal

RUN apk update --no-cache && \
    apk add --no-cache --virtual .build-deps gcc python3-dev libc-dev libffi-dev openssl-dev

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && rm -rf /var/cache/apk/*

RUN adduser -D -H -h /opt/fotogal fotogal
COPY --chown=fotogal:fotogal ./fotogal /opt/fotogal/
USER fotogal

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]