FROM ubuntu:20.04
MAINTAINER Sam Kinn <samk@alleninstitute.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip nginx gunicorn supervisor

RUN mkdir -p /var/log/api
COPY conf/supervisor.conf /etc/supervisor/conf.d/webapp.conf

# Setup application
RUN mkdir -p /api
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt

CMD ["/usr/bin/supervisord", "-nc", "/etc/supervisor/supervisord.conf"]