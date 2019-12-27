FROM python:3.6

COPY ./src/datastorage /www/app/datastorage
COPY ./src/requirements.txt /www/app/datastorage/requirements.txt
COPY ./docker/settings_local.py /www/app/datastorage/settings_local.py
COPY ./docker/gunicorn.py /www/app/datastorage/gunicorn.py

WORKDIR /www/app/datastorage

RUN pip install -r requirements.txt && \
    pip install gunicorn==19.9.0 gevent==1.4.0 && \
    SKIP_INIT=1 python manage.py collectstatic --noinput