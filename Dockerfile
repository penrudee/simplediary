FROM python:slim

RUN useradd pharmbook

WORKDIR /home/pharmbookdiary

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY wsgi.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP wsgi.py

RUN chown -R pharmbook:pharmbook ./
USER pharmbook

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]