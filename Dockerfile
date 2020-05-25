FROM python:3.8

RUN mkdir /root/app
COPY wolservice /root/app/wolservice
COPY setup.py /root/app
COPY extra/* /root/app
COPY requirements.txt /root/app

RUN pip install --no-cache-dir /root/app
RUN pip install uwsgi

EXPOSE 8080
CMD ["/bin/bash", "-c", "cd /root/app && uwsgi --ini config.ini"]
