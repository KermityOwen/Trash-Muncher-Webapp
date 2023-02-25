FROM python:3

ENV PYTHONUNBUFFERED1
RUN mkdir /code
WORKDIR /code
COPY . /src/
RUN pip install -r requirements.txt
