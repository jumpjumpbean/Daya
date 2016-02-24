# gunicorn-flask

FROM ubuntu:12.04
MAINTAINER Niu Feng <jumpbeandev@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-utils \
        autoconf \
        automake \
        file \
        g++ \
        gcc \
        make \
        patch \
        libssl-dev \
        libffi-dev

RUN apt-get install -y --no-install-recommends libevent-dev
RUN apt-get install -y python python-dev python-pip python-virtualenv gunicorn
RUN rm -rf /var/lib/apt/lists/*

# Setup flask application
#RUN mkdir -p /deploy/app
COPY gunicorn_config.py /var/www/gunicorn_config.py
COPY daya /var/www/app
RUN pip install -r /var/www/app/requirements.txt
RUN pip install greenlet eventlet gevent 
WORKDIR /var/www/app

EXPOSE 5000

# Start gunicorn
CMD ["/usr/bin/gunicorn", "--config", "/var/www/gunicorn_config.py", "run_server:app"]
