FROM python:3.7

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip nginx gunicorn supervisor

RUN mkdir -p /var/log/webapp
COPY conf/supervisor.conf /etc/supervisor/conf.d/webapp.conf

# Setup application
RUN mkdir -p /webapp
WORKDIR /webapp
COPY . /webapp
RUN pip install -r requirements.txt

CMD ["/usr/bin/supervisord", "-nc", "/etc/supervisor/supervisord.conf"]