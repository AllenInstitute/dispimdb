# FROM ubuntu:20.04
# MAINTAINER Sam Kinn <samk@alleninstitute.org>

# ENV DEBIAN_FRONTEND noninteractive

# RUN apt-get update
# RUN apt-get install -y python python-pip python-virtualenv nginx gunicorn supervisor

# # Setup application
# RUN mkdir -p /app
# COPY app /app
# RUN pip install -r /app/requirements.txt

# # Setup nginx
# RUN rm /etc/nginx/sites-enabled/default
# COPY acworkflow.conf /etc/nginx/sites-available
# RUN ln -s /etc/nginx/sites-available/acworkflow.conf /etc/nginx/sites-available/acworkflow.conf
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# # Setup supervisord
# RUN mkdir -p /var/log/supervisor
# COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# COPY conf/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# # Start processes
# CMD ["/usr/bin/supervisord"]

FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["./flask_run.sh"]