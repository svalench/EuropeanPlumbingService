FROM python:3.11-alpine
RUN mkdir /code
WORKDIR /code
COPY . /code
# nginx
RUN apk add nginx && apk add openrc
RUN mkdir /run/openrc
COPY ./dockers/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./dockers/nginx/plumping.nginx.conf /etc/nginx/sites-available/plumping.nginx.conf
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/plumping.nginx.conf /etc/nginx/sites-enabled/
RUN nginx -t
#RUN nginx -s reload
# uwsgi setup
RUN mkdir /tmp/uwsgi/
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
RUN pip install -r requirements.txt
# utils
RUN apk add nano
RUN apk add lsof && apk add net-tools
RUN ls -la /run/
CMD ["uwsgi", "--ini", "/code/pumping.uwsgi.ini"]