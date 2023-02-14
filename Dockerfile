FROM python:3.10-slim-buster
ENV PYTHONNUNBUFFERED=1
WORKDIR /allergie
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt