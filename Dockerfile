FROM python:3.8

RUN mkdir /usr/src/app
COPY wolservice /usr/src/app/wolservice
COPY setup.py /usr/src/app
COPY extra/* /usr/src/app
COPY requirements.txt /usr/src/app

RUN ls /usr/src/app
RUN pip install --no-cache-dir /usr/src/app
RUN pip install uwsgi

EXPOSE 8080
CMD ["/bin/bash", "-c", "cd /usr/src/app && uwsgi --ini config.ini"]
