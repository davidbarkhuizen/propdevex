sudo mkdir /var/www/sdmm

sudo mkdir /var/www/sdmm/media
sudo mkdir /var/www/sdmm/media/frp
sudo mkdir /var/www/sdmm/media/frp/image
sudo mkdir /var/www/sdmm/media/frp/json

sudo cp ../config.json.template /var/www/sdmm/config.json

sudo cp -R ../django_web_server /var/www/sdmm/django_web_server

sudo cp -R ../import /var/www/sdmm/

sudo cp -R ../dal /var/www/sdmm/dal
sudo cp -R ../siteupdater /var/www/sdmm/siteupdater
sudo cp -R ../import /var/www/sdmm/import

sudo cp ../*.py /var/www/sdmm/

sudo mkdir /var/log/sdmm/



