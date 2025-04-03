#!/bin/sh

envsubst '$BILLUMY_AUTH_TOKEN' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
exec nginx -g 'daemon off;'