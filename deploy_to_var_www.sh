sudo mkdir /var/www/sdmm

sudo mkdir /var/www/sdmm/media
sudo mkdir /var/www/sdmm/media/frp
sudo mkdir /var/www/sdmm/media/frp/image
sudo mkdir /var/www/sdmm/media/frp/json


sudo cp -f config.json.template /var/www/sdmm/config.json.template

sudo rm -Rf /var/www/sdmm/django_web_server
sudo cp -Rf django_web_server /var/www/sdmm/django_web_server

sudo rm -Rf /var/www/sdmm/import
sudo cp -Rf import /var/www/sdmm/import

sudo rm -Rf /var/www/sdmm/dal
sudo cp -Rf dal /var/www/sdmm/dal

sudo rm -Rf /var/www/sdmm/siteupdater
sudo cp -Rf siteupdater /var/www/sdmm/siteupdater

sudo rm -Rf /var/www/sdmm/import
sudo cp -Rf import /var/www/sdmm/import

sudo cp *.py /var/www/sdmm/

sudo mkdir /var/log/sdmm/



