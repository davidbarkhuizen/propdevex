echo 'RE-INIT SDMM DATABASE'
read -r -p "Are you sure? [y/N] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]
then
	echo 'dropping database sdmm...'
	sudo -u postgres dropdb sdmm
	echo 'database sdmm dropped.'

	echo 'dropping user sdmm...'
	sudo -u postgres dropuser sdmm
	echo 'user sdmm dropped'

	echo 'creating user sdmm...'
	sudo -u postgres createuser sdmm -P
	echo 'user sdmm created.'

	echo 'creating sdmm database owned by user sdmm...'
	sudo -u postgres createdb sdmm -O sdmm
	echo 'done!'

	echo 'initiating ORM db initialization...'
	cd ../django_web_server
	sudo python manage.py syncdb
	echo 'synced.'
else
	echo 'aborted'
fi