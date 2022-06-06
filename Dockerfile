FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev \
    freetype-dev msttcorefonts-installer
RUN update-ms-fonts
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir /app
COPY ./app /app
WORKDIR /app