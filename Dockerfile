FROM python:3.11
RUN mkdir /code
WORKDIR /code
COPY . /code
COPY dockers/entrypoint.sh /code/
# nginx
RUN apt update -y && apt install nginx -y
RUN mkdir /run/openrc
COPY ./dockers/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./dockers/nginx/plumping.nginx.conf /etc/nginx/sites-available/plumping.nginx.conf
RUN ln -s /etc/nginx/sites-available/plumping.nginx.conf /etc/nginx/sites-enabled/
RUN nginx -t

# uwsgi setup
RUN mkdir /tmp/uwsgi/
#RUN apt install python3-dev build-base pcre-dev
RUN pip install uwsgi
RUN pip install -r requirements.txt

# utils
RUN apt install nano
RUN apt install lsof && apt install net-tools
RUN ls -la /run/

EXPOSE 8081
RUN ["chmod", "+x", "/code/entrypoint.sh"]
ENTRYPOINT '/code/entrypoint.sh'
#CMD ["uwsgi", "--ini", "/code/pumping.uwsgi.ini"]