
rm django_web_server/static/data/*.*
rm django_web_server/static/data/image/*.*

cp media/frp/* django_web_server/static/data/
cp media/frp/image/*.* django_web_server/static/data/image/
cp media/frp/json/*.*  django_web_server/static/data/
