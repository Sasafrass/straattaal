FROM python:3.8-slim-buster

RUN useradd slang

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN mkdir /harkema/pip
RUN venv/bin/pip install TMPDIR=/harkema/pip --cache-dir=/harkema/pip --build /harkema/pip -r requirements.txt
RUN venv/bin/pip install --no-cache-dir gunicorn

COPY app app
COPY migrations migrations
COPY straattaal.py config.py boot.sh ./
RUN chmod +x boot.sh
COPY data data

ENV FLASK_APP straattaal.py

RUN chown -R slang:slang ./
USER slang

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
