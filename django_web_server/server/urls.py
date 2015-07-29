from django.conf.urls import url

from ctrl import sites

urlpatterns = [
		url(r'^admin/sites', sites.routing),
		url(r'^admin/sites$', sites.routing),
	]
