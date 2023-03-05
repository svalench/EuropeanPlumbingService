#!/bin/bash
service nginx start
nginx -s reload
python /code/manage.py collectstatic
uwsgi --ini /code/pumping.uwsgi.ini