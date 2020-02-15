#!/bin/sh

run_server()
{
	if [ ! -d /var/www/html/data ]
	then
		mkdir /var/www/html/data
	fi

	curl https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml > /var/www/html/data/rates.xml
	python3 webapp/manage.py runserver 0:8000
}

if [ -f /var/www/html/webapp/manage.py ]
then
	run_server
else 
	django-admin startproject webapp
	run_server
fi
