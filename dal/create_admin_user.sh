echo "from django.contrib.auth.models import User; 
User.objects.create_superuser('root', 'sdmm@gmail.com', 'password')
" | python ../django_web_server/manage.py shell