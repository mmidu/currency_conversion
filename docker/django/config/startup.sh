#!/bin/sh

run_server()
{
	if [ ! -d /var/www/html/data ]
	then
		mkdir /var/www/html/data
	fi

	curl https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml > /var/www/html/data/rates.xml
	python3 /var/www/html/$PROJECT_NAME/manage.py runserver 0:8000
}

if [ -f /var/www/html/$PROJECT_NAME/manage.py ]
then
	run_server
else 
	django-admin startproject $PROJECT_NAME
	cd $PROJECT_NAME
	python3 /var/www/html/$PROJECT_NAME/manage.py startapp convert
	run_server
fi
