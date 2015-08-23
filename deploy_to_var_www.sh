sudo mkdir /var/www/sdmm

sudo mkdir /var/www/sdmm/media
sudo mkdir /var/www/sdmm/media/frp
sudo mkdir /var/www/sdmm/media/frp/image
sudo mkdir /var/www/sdmm/media/frp/json

sudo cp -f config.json.template /var/www/sdmm/config.json.template

sudo cp -Rf django_web_server /var/www/sdmm/django_web_server

sudo cp -Rf import /var/www/sdmm/

sudo cp -Rf dal /var/www/sdmm/dal
sudo cp -Rf siteupdater /var/www/sdmm/siteupdater
sudo cp -Rf import /var/www/sdmm/import

sudo cp *.py /var/www/sdmm/

sudo mkdir /var/log/sdmm/



