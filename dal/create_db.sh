read -r -p "Are you sure? [y/N] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]
then
	echo 'dropping and re-creating database and user' 
	sudo -u postgres dropdb sdmm
	sudo -u postgres dropuser sdmm
	sudo -u postgres createuser sdmm -P
	sudo -u postgres createdb sdmm -O sdmm
	echo 'done'

	cd ../django_web_server
	sudo python manage.py syncdb
fi