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
RUN pip install uwsgi
RUN pip install -r requirements.txt

# utils
RUN apt install nano
RUN apt install lsof && apt install net-tools
RUN ls -la /run/

# env var
ARG PROD
ARG API_KIT_SERVICE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV PROD=${PROD}
ENV API_KIT_SERVICE=${API_KIT_SERVICE}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

EXPOSE 8081
RUN ["chmod", "+x", "/code/entrypoint.sh"]
ENTRYPOINT '/code/entrypoint.sh'
#CMD ["uwsgi", "--ini", "/code/pumping.uwsgi.ini"]