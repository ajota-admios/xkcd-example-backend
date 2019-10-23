FROM python:3.8

MAINTAINER AJ Ortiz "ajota.os@icloud.com"

WORKDIR /var/app

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

CMD python ./main.py
