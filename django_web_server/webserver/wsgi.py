'''


import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
'''

import os, sys

sys.path.append('/home/david/code/propdevex/github/django_web_server/')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
