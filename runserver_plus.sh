#!/bin/sh
if [ -n "$1" ]; then
	./manage.py runserver_plus $1
else
	./manage.py runserver_plus
fi
