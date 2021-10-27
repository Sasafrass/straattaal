FROM python:3.6-slim-buster

RUN useradd slang

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev

RUN venv/bin/pip install --no-cache-dir -r requirements.txt
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
